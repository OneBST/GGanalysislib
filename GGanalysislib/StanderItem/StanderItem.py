from GGanalysislib.PityGacha import *

class StanderItem(PityGacha):
    # 调用动态链接库DP
    def get_distribution(self, item_num=1, calc_pull=270, pull_state=0):  
        # 调用动态链接库
        Objdll = LoadDLL()
        dp_shape = [item_num+1, calc_pull+1]
        dp_ans = np.zeros(dp_shape, dtype=float)
        # 获取ctypes指针
        ans_ptr = dp_ans.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        hit_p_ptr = self.hit_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        Objdll.GI_stander_DP(   ans_ptr,                            # DP结果存放数组
                                item_num,                           # 计算物品抽取数量
                                calc_pull,                          # 计算抽取次数
                                pity_p_ptr,                         # 概率提升表
                                self.pity_pos,                      # 保底抽数
                                hit_p_ptr,                          # 类别概率表
                                self.hit_pos,                       # 类别保底
                                pull_state,                         # 垫抽情况
                                self.type_state,                    # 多少抽没有另一类物品
                                self.last_type,                     # 上次五星种类
                                self.stander_num,                   # 常驻池中本类物品数量
                                self.collect_all)                   # 是否计算收集齐全概率
        return dp_ans
    # 模拟方法 用于检查DP正确性
    def simulate_pull_stander(self, pull_state=0, end_pos=300, pull_num = 1):
        import random
        counter = 0  # 抽数计数器
        item_counter = 0  # 物品计数器
        # 处理初始条件
        if self.last_type == 0:  # 上抽是本类
            want_state = pull_state
            other_state = self.type_state
        else:  # 上抽是异类
            want_state = self.type_state
            other_state = pull_state
        while counter<end_pos:
            want_state += 1
            other_state += 1
            counter += 1
            pull_state += 1
            p_get = 1/self.stander_num  # 得到想要物品概率
            if self.collect_all:  # 如果是收集齐全物品
                p_get = (self.stander_num - item_counter) / self.stander_num
            # 抽到了物品
            if self.pity_p[pull_state] >= random.random():
                pull_state = 0
                get_mark = 0
                # 判断类别
                if want_state > self.hit_pos:
                    get_mark = 1
                elif other_state > self.hit_pos:
                    get_mark = 0
                else:
                    if want_state > other_state:
                        if self.hit_p[want_state] >= random.random():
                            get_mark = 1
                    else:
                        if 1 - self.hit_p[other_state] >= random.random():
                            get_mark = 1
                # 结算具体抽到的物品
                if get_mark:  # 抽到本类
                    want_state = 0
                    if p_get >= random.random():
                        item_counter += 1
                        if item_counter == pull_num:
                            return counter
                else:
                    other_state = 0
        # 限界模拟到end_pos
        return counter
    # 设置平稳参数
    def init_hit_p(self):
        self.hit_p = np.zeros(self.hit_pos+1, dtype=float)
        for i in range(1, 148):
            self.hit_p[i] = 0.5
        for i in range(148, 181):
            self.hit_p[i] = (0.03 * (i-147) + 0.003) / min(1, 0.03 * (i-147) + 0.006)
    # 常数设置
    def set_const(self):
        # 保底参数
        self.pity_pos = 90          # 保底位置
        self.hit_pos = 180          # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 5        # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关
    # 初始化函数
    def __init__(self):
        # 设置常数
        self.set_const()
        # 计算基本参数
        self.init_pity_p()          # 初始化概率提升表
        self.init_hit_p()           # 初始化类别概率保底提升表
        self.init_item_statistics() # 初始化物品抽取统计量