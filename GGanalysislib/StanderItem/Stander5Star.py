from GGanalysislib.StanderItem.StanderItem import StanderItem

class Stander5Star(StanderItem):
    pass

class Stander5StarCharacter(Stander5Star):
    def init_pity_p(self):
        self.pity_p = self.common_5star_pity()
    def set_const(self):
        # 保底参数
        self.pity_pos = 90          # 保底位置
        self.hit_pos = 180          # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 5        # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关

class Stander5StarWeapon(Stander5Star):
    def set_const(self):
        # 保底参数
        self.pity_pos = 90          # 保底位置
        self.hit_pos = 180          # 类别保底位置

        # 普池参数
        self.last_type = 0          # 上次抽到物品种类 0表示本类 1表示异类
        self.type_state = 0         # 多少抽没有另一类物品
        self.stander_num = 10       # 常驻池中本类别物品数量
        self.collect_all = 0        # 计算抽齐各类物品概率开关