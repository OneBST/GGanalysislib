from GGanalysislib.UpItem.UpItem import UpItem
import numpy as np

class Up4starCharacter(UpItem):
    # 对于UP四星进行了简化，忽略了五星及常驻四星对其的影响，造成计算概率略低
    def init_pity_p(self):
        self.pity_p = self.common_4star_pity()
    def set_const(self):
        # 保底参数
        self.pity_pos = 10          # 保底位置
        self.up_rate = 0.5          # UP概率
        self.up_type = 3            # UP物品数量

        # 普池默认参数 默认UP物品均不在普池
        self.want_in_stander = 0    # 想要的是否在常驻
        self.up_in_stander = 0      # UP物品在常驻池中的数量
        self.stander_num = 1        # 常驻池中物品数量