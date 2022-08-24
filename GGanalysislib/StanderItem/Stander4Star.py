import numpy as np
from GGanalysislib.StanderItem.StanderItem import StanderItem

class Stander4Star(StanderItem):
    # 对于UP四星进行了简化，忽略了五星及常驻四星对其的影响，造成计算概率略低
    def init_pity_p(self):
        self.pity_p = self.common_4star_pity()
    # 设置平稳参数
    def init_hit_p(self):
        self.hit_p = np.zeros(self.hit_pos+1, dtype=float)
        for i in range(1, 18):
            self.hit_p[i] = 0.5
        for i in range(18, 21):
            self.hit_p[i] = (0.255 * (i-17) + 0.0255) / min(1, 0.255 * (i-17) + 0.0255*2)
    def set_const(self):
        # 保底参数
        self.pity_pos = 10          # 保底位置
        self.hit_pos = 20           # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 27       # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关

class Stander4StarCharacter(Stander4Star):
    def set_const(self):
        # 保底参数
        self.pity_pos = 10          # 保底位置
        self.hit_pos = 20           # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 27       # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关

class Stander4StarWeapon(Stander4Star):
    def set_const(self):
        # 保底参数
        self.pity_pos = 10          # 保底位置
        self.hit_pos = 20           # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 18       # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关