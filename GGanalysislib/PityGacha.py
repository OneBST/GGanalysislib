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
        # 改为77保底
        pity_p = np.zeros(78, dtype=float)
        for i in range(1, 63):
            pity_p[i] = 0.007
        for i in range(63, 77):
            pity_p[i] = pity_p[i-1] + 0.07
        pity_p[77] = 1
        return pity_p
    # 四星武器保底概率提升表
    @classmethod
    def weapon_4star_pity(cls):
        pity_p = np.zeros(10, dtype=float)
        for i in range(1, 8):
            pity_p[i] = 0.06
        pity_p[8] = 0.66
        pity_p[9] = 1   
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
    @classmethod
    def calc_pull_expectation_solve_equation(cls, pity_p):
        pity_pos = len(pity_p)-1
        # 构造矩阵
        M = np.zeros((pity_pos, pity_pos), dtype=float)
        for i in range(1, pity_pos):
            M[i][i-1] = 1 - pity_p[i]
        for i in range(pity_pos):
            M[0][i] = pity_p[i+1]
        M = M - np.identity(pity_pos)   # 减去对角阵
        M[pity_pos-1] = 1               # 末行设置为1
        # 设置向量
        X = np.zeros(pity_pos, dtype=float)
        X[pity_pos-1] = 1
        # 解线性方程求解
        ans = np.linalg.solve(M, X)
        return 1/ans[0]
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
    def luck_evaluate(self, get_num, use_pull, left_pull=0):
        # 调用动态链接库
        Objdll = LoadDLL()
        Objdll.rank_common_item.restype = ctypes.c_double
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return Objdll.rank_common_item(
            get_num,            #已有物品抽取数量
            use_pull,          #总共抽取次数
            left_pull,          #距离获得上个物品又抽了多少
            pity_p_ptr,         #概率提升表
            self.pity_pos)      #保底抽数
                
    # 模拟一下看看运气评价对不对
    def simulate_luck(self, item_num, use_pull, left_pull):
        import random
        pull_state = 0  #状态记录器
        item_counter = 0  # 物品计数器
        for i in range(use_pull):
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
        if pull_state >= left_pull:  # 剩下抽数多或相同
            return 0  # 运气更好或相同
        return 1  # 运气更差
    def set_const(self):
        self.pity_pos = 90  # 保底位置
    def __init__(self):
        # 设置常数
        self.set_const()
        # 计算基本参数
        self.init_pity_p()          # 初始化概率提升表
        self.init_item_statistics() # 初始化物品抽取统计量
