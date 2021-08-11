from GGanalysislib.UpItem.Up5starWeaponOld import Up5starWeaponOld
from GGanalysislib.PityGacha import LoadDLL
import numpy as np
import ctypes

class Up5starWeaponEP(Up5starWeaponOld):
    # 采用神铸定轨的武器池
    # 调用动态链接库DP
    def get_distribution(self, item_num=1, calc_pull=240, pull_state=0, up_guarantee=0):  
        # 调用动态链接库
        Objdll = LoadDLL()
        dp_shape = [item_num+1, calc_pull+1]
        dp_ans = np.zeros(dp_shape, dtype=float)
        # 获取ctypes指针
        ans_ptr = dp_ans.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        pity_p_ptr = self.pity_p.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        Objdll.GI_weapon_EP_DP( ans_ptr,                            # DP结果存放数组
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
    def calc_reference_upitem_expectation(self):
        # 这里直接套用结论值
        return self.item_expectation/0.5039
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
                if up_guarantee == 3:  # 命定值保底
                    return counter
                # 抽到了UP
                if up_guarantee == 2 or self.up_rate >= random.random():
                    # 没歪
                    if 1/self.up_type >= random.random():
                        return counter
                    # 歪了
                    if up_guarantee == 0:
                        up_guarantee = 1
                    else:
                        up_guarantee = 3
                    continue
                # 以下必为0和1状态对应执行的
                # 第一次没有抽到UP 但常驻中抽到了想要的UP
                if self.want_in_stander/self.stander_num >= random.random():
                    return counter
                # 常驻中没有抽到想要的UP 但是抽到了其他UP
                if (self.up_in_stander-self.want_in_stander)/max(1, (self.stander_num-self.want_in_stander)) >= random.random():
                    if up_guarantee == 0:
                        up_guarantee = 1
                    else:
                        up_guarantee = 3 
                else:
                    if up_guarantee == 0:
                        up_guarantee = 2
                    else:
                        up_guarantee = 3 
        # 限界模拟到end_pos
        return counter