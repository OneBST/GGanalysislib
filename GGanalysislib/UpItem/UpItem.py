from GGanalysislib.PityGacha import *

class UpItem(PityGacha):
    # 调用动态链接库DP
    def get_distribution(self, item_num=1, calc_pull=180, pull_state=0, up_guarantee=0):  
        # 调用动态链接库
        Objdll = LoadDLL()
        dp_shape = [item_num+1, calc_pull+1]
        dp_ans = np.zeros(dp_shape, dtype=float)
        # 获取ctypes指针
        ans_ptr = dp_ans.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        Objdll.GI_upitem_DP(ans_ptr,                            # DP结果存放数组
                            item_num,                           # 计算物品抽取数量
                            calc_pull,                          # 计算抽取次数
                            pity_p_ptr,                         # 概率提升表
                            self.pity_pos,                      # 保底抽数
                            ctypes.c_double(self.up_rate),      # UP概率
                            self.up_type,                       # UP物品种类
                            pull_state,                         # 垫抽情况
                            up_guarantee,                       # 大保底情况
                            self.want_in_stander,               # 想要的是否在常驻
                            self.up_in_stander,                 # UP物品在常驻池中的数量
                            self.stander_num)                   # 常驻池中物品数量
        return dp_ans
    # 概率计算
    def get_p(self, item_num, calc_pull, pull_state=0, up_guarantee=0):
        dp_ans = self.get_distribution(item_num, calc_pull, pull_state, up_guarantee)[item_num][:]
        dp_ans = dp_ans.cumsum()
        return dp_ans[calc_pull]
    # 模拟方法 用于检查DP正确性
    def simulate_pull(self, pull_state=0, up_guarantee=0, end_pos=300):
        import random
        counter = 0
        while counter<end_pos:
            counter += 1
            pull_state += 1
            # 抽到了物品
            if self.pity_p[pull_state] >= random.random():
                pull_state = 0
                # 抽到了UP
                if up_guarantee or self.up_rate >= random.random():
                    # 没歪
                    if 1/self.up_type >= random.random():
                        return counter
                    # 歪了
                    up_guarantee = 0
                    continue
                # 第一次没有抽到UP 但常驻中抽到了想要的UP
                if self.want_in_stander/self.stander_num >= random.random():
                    return counter
                # 常驻中没有抽到想要的UP 但是抽到了其他UP
                if (self.up_in_stander-self.want_in_stander)/max(1, (self.stander_num-self.want_in_stander)) >= random.random():
                    up_guarantee = 0
                else:
                    up_guarantee = 1
        # 限界模拟到end_pos
        return counter

    def calc_reference_upitem_expectation(self):
        return (2 - self.up_rate) * self.up_type * self.item_expectation
    
    # 计算条件期望
    def calc_conditional_expectation(self):
        self.C_expactation = np.zeros(self.pity_pos, dtype=float)
        self.C_expactation[self.pity_pos-1] = 1
        for i in range(self.pity_pos-2, -1, -1):
            self.C_expactation[i] = (self.C_expactation[i+1]+1) * (1-self.pity_p[i+1]) + self.pity_p[i+1]
    
    # 物品抽取基本统计量
    def init_item_statistics(self):
        # 分布列
        self.item_distribution = self.calc_simple_distribution(self.pity_p)
        # 本等级物品的期望
        self.item_expectation = self.calc_pull_expectation(self.item_distribution)
        # 抽取本等级物品的方差
        self.item_variance = self.calc_pull_variance(self.item_distribution)
        # 抽取UP物品参考期望
        self.reference_upitem_expectation = self.calc_reference_upitem_expectation()
        # 计算条件期望
        self.calc_conditional_expectation()
    def set_const(self):
        # 保底参数
        self.pity_pos = 90          # 保底位置
        self.up_rate = 0.5          # UP概率
        self.up_type = 1            # UP物品数量

        # 普池默认参数 默认UP物品均不在普池
        self.want_in_stander = 0    # 想要的是否在常驻
        self.up_in_stander = 0      # UP物品在常驻池中的数量
        self.stander_num = 1        # 常驻池中物品数量