import numpy as np
import ctypes
import sys

def LoadDLL():  # Python3.8后Windows下加载动态链接库的安全性更新
    if sys.platform == "win32":  # windows下的动态链接库
        return ctypes.CDLL("./GGanalysislib/bin/GGanalysis.dll")  # 指明具体位置
    else:  # 其他系统加载文件
        return ctypes.CDLL("./GGanalysislib/bin/libGGanalysis.so")  # 指明具体位置

class PityGacha():
    # 普通五星保底概率提升表
    @classmethod
    def common_5star_pity(cls):
        pity_p = np.zeros(91, dtype=float)
        for i in range(1, 74):
            pity_p[i] = 0.006
        for i in range(74, 91):
            pity_p[i] = 0.06 + pity_p[i-1]
        pity_p[90] = 1
        return pity_p
    # 普通四星保底概率提升表
    @classmethod
    def common_4star_pity(cls):
        pity_p = np.zeros(11, dtype=float)
        for i in range(1, 9):
            pity_p[i] = 0.051
        pity_p[9] = 0.561
        pity_p[10] = 1
        return pity_p
    # 五星武器保底概率提升表
    @classmethod
    def weapon_5star_pity(cls):
        pity_p = np.zeros(81, dtype=float)
        for i in range(1, 63):
            pity_p[i] = 0.007
        for i in range(63, 74):
            pity_p[i] = pity_p[i-1] + 0.07
        for i in range(74, 80):
            pity_p[i] = pity_p[i-1] + 0.035
        pity_p[80] = 1
        return pity_p
    # 四星武器保底概率提升表
    @classmethod
    def weapon_4star_pity(cls):
        pity_p = np.zeros(11, dtype=float)
        for i in range(1, 8):
            pity_p[i] = 0.06
        pity_p[8] = 0.66
        pity_p[9] = 0.96   
        pity_p[10] = 1
        return pity_p
        
    def init_pity_p(self):  # 初始化概率提升表，继承时候需要重写
        self.pity_p = self.common_5star_pity()
    
    # 物品抽取分布列
    @classmethod
    def calc_simple_distribution(cls, pity_p):
        item_distribution = np.zeros(len(pity_p), dtype=float)
        temp_state = 1
        for i in range(1, len(pity_p)):
            item_distribution[i] = temp_state * pity_p[i]
            temp_state = temp_state * (1-pity_p[i])
        return item_distribution
    # 物品抽取期望抽数
    @classmethod
    def calc_pull_expectation(cls, item_distribution):
        item_expectation = 0
        for i in range(1, len(item_distribution)):
            item_expectation += item_distribution[i] * i
        return item_expectation
    # 物品抽取抽数方差
    @classmethod
    def calc_pull_variance(cls, item_distribution):
        item_variance = 0
        item_expectation = cls.calc_pull_expectation(item_distribution) 
        for i in range(1, len(item_distribution)):
            item_variance += item_distribution[i] * (i - item_expectation) ** 2
        return item_variance
    # 物品抽取基本统计量
    def init_item_statistics(self):
        # 分布列
        self.item_distribution = self.calc_simple_distribution(self.pity_p)
        # 本等级物品的期望
        self.item_expectation = self.calc_pull_expectation(self.item_distribution)
        # 抽取本等级物品的方差
        self.item_variance = self.calc_pull_variance(self.item_distribution)
    # 调用动态链接库DP
    def get_distribution(self, item_num=1, calc_pull=270, pull_state=0):
        # 调用动态链接库
        Objdll = LoadDLL()
        dp_shape = [item_num+1, calc_pull+1]
        dp_ans = np.zeros(dp_shape, dtype=float)
        # 获取ctypes指针
        ans_ptr = dp_ans.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        Objdll.pity_item_DP(ans_ptr,                            # DP结果存放数组
                            item_num,                           # 计算物品抽取数量
                            calc_pull,                          # 计算抽取次数
                            pity_p_ptr,                         # 概率提升表
                            self.pity_pos,                      # 保底抽数
                            pull_state)                         # 垫抽情况
        return dp_ans
    # 概率计算
    def get_p(self, item_num, calc_pull, pull_state=0):
        dp_ans = self.get_distribution(item_num, calc_pull, pull_state)[item_num][:]
        dp_ans = dp_ans.cumsum()
        return dp_ans[calc_pull]
    
    # 简单的运气评价 看看超过了%多少人 仅仅适用于五星数量衡量
    def luck_evaluate(self, item_num, use_pull, leave_pull):
        dp_ans = self.get_distribution(item_num, use_pull, 0)
        # 计算 “没抽到” 辅助数组oops
        oops = np.zeros(self.pity_pos+1, dtype=float)
        temp_state = 1
        oops[0] = 1
        for i in range(1, self.pity_pos+1):
            temp_state = temp_state * (1 - self.pity_p[i])
            oops[i] = temp_state
        luck_check_shape = [item_num+1, self.pity_pos+1]
        luck_check = np.zeros(luck_check_shape, dtype=float)
        ans = 0  # 记录超越了多少人
        dp_ans[0][0] = 1  # 修正0处
        for i in range(item_num+1):  # 抽了多少个
            calc_end_pos = 90
            if i == item_num:
                calc_end_pos = leave_pull
            for j in range(calc_end_pos):  # 额外垫了多少抽
                # print('五星数'+str(i)+' 垫抽数'+str(j))
                if use_pull-j < 0:
                    break
                ans += dp_ans[i][use_pull-j] * oops[j]
        return ans
    
    # 模拟一下看看运气评价对不对
    def simulate_luck(self, use_pull, item_num, leave_pull):
        import random
        counter = 0  # 抽数计数器
        pull_state = 0  #状态记录器
        item_counter = 0  # 物品计数器
        while counter <= use_pull:
            counter += 1
            pull_state += 1
            # 抽到了物品
            if self.pity_p[pull_state] >= random.random():
                pull_state = 0
                item_counter += 1
                # 比设定值更好的情况
                if item_counter > item_num:
                    return 0
        if item_counter < item_num:
            return 1  # 运气更差
        if pull_state > leave_pull:
            return 0  # 运气更好
        return 1  # 运气相同或者更差
    def set_const(self):
        self.pity_pos = 90  # 保底位置
    def __init__(self):
        # 设置常数
        self.set_const()
        # 计算基本参数
        self.init_pity_p()          # 初始化概率提升表
        self.init_item_statistics() # 初始化物品抽取统计量
