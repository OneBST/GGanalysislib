from GGanalysislib.UpItem.UpItem import UpItem
import numpy as np

class Up5starWeaponOld(UpItem):
    # 没有神铸定轨的武器池
    def init_pity_p(self):
        self.pity_p = np.zeros(self.pity_pos+1, dtype=float)
        for i in range(1, 63):
            self.pity_p[i] = 0.007
        for i in range(63, 74):
            self.pity_p[i] = self.pity_p[i-1] + 0.07
        for i in range(74, 80):
            self.pity_p[i] = self.pity_p[i-1] + 0.035
        self.pity_p[80] = 1
    def set_const(self):
        # 保底参数
        self.pity_pos = 80          # 保底位置
        self.up_rate = 0.75         # UP概率
        self.up_type = 2            # UP物品数量

        # 普池默认参数 默认UP物品均不在普池
        self.want_in_stander = 0    # 想要的是否在常驻
        self.up_in_stander = 0      # UP物品在常驻池中的数量
        self.stander_num = 1        # 常驻池中物品数量
