from GGanalysislib.UpItem.UpItem import UpItem
from GGanalysislib.PityGacha import *

class Up5starCharacter(UpItem):
    def init_pity_p(self):
        self.pity_p = self.common_5star_pity()
    # 简单的运气评价 看看超过了%多少人 仅仅适用于UP五星角色数量衡量
    def luck_evaluate(self, get_num, use_pull, left_pull=0, up_guarantee=0):
        # 调用动态链接库
        Objdll = LoadDLL()
        Objdll.rank_up_item.restype = ctypes.c_double
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return Objdll.rank_up_item(
            get_num,                            # 已有物品抽取数量
            use_pull,                          # 总共抽取次数
            left_pull,                          # 距离获得上个物品又抽了多少
            up_guarantee,                       # 大保底情况
            pity_p_ptr,                         # 概率提升表
            self.pity_pos,                      # 保底抽数
            ctypes.c_double(self.up_rate),      # UP概率
            self.up_type)                       # UP物品种类
    
    # 计算当前情况下抽到下一个UP物品需要的抽数期望
    def calc_case_expectation(self, left_pull, up_guarantee):
        # 这段计算代码的说明见./source/LuckyRank.c 内rank_up_item函数
        if up_guarantee == 0:
            case_e = (  self.up_rate / self.up_type * self.C_expactation[left_pull] + 
                        self.up_rate * ((self.up_type-1)/self.up_type) * (self.C_expactation[left_pull] + self.reference_upitem_expectation) + 
                        (1-self.up_rate) * (1/self.up_type) * (self.C_expactation[left_pull] + self.C_expactation[0]) +
                        (1-self.up_rate) * ((self.up_type-1)/self.up_type) * (self.C_expactation[left_pull] + self.C_expactation[0] + self.reference_upitem_expectation)
            )
        else:
            case_e = (  1/self.up_type * self.C_expactation[left_pull] + 
                        ((self.up_type-1)/self.up_type) * (self.C_expactation[left_pull] + self.reference_upitem_expectation)
            )
        return case_e
    
    # 模拟一下看看运气评价对不对
    def simulate_luck(self, item_num, use_pull, left_pull, test_up_guarantee):
        import random
        pull_state = 0  #状态记录器
        item_counter = 0  # 物品计数器
        up_guarantee = 0  # 保留原始值
        for i in range(use_pull):
            pull_state += 1
            # 抽到了物品
            if self.pity_p[pull_state] >= random.random():
                pull_state = 0
                # 抽到了UP物品
                if up_guarantee or random.random()<=self.up_rate:
                    up_guarantee = 0
                    if random.random() <= 1/self.up_type:
                        item_counter += 1
                else:
                    up_guarantee = 1
                # 比设定值更好的情况
                if item_counter > item_num:
                    return 0
        if item_counter < item_num:
            return 1  # 模拟情况运气更差
        # 抽到的UP物品数量相同，根据再抽一个的期望判断
        test_e = self.calc_case_expectation(left_pull, test_up_guarantee)
        case_e = self.calc_case_expectation(pull_state, up_guarantee)
        if test_e >= case_e:  # 模拟情况更优或一样优
            return 0
        return 1  # 模拟情况运气更差