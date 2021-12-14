from GGanalysislib.UpItem.UpItem import UpItem
import numpy as np

class Up5starWeaponOld(UpItem):
    # 没有神铸定轨的武器池
    def init_pity_p(self):
        self.pity_p = self.weapon_5star_pity()
    def set_const(self):
        # 保底参数
        self.pity_pos = 77          # 保底位置
        self.up_rate = 0.75         # UP概率
        self.up_type = 2            # UP物品数量

        # 普池默认参数 默认UP物品均不在普池
        self.want_in_stander = 0    # 想要的是否在常驻
        self.up_in_stander = 0      # UP物品在常驻池中的数量
        self.stander_num = 1        # 常驻池中物品数量
