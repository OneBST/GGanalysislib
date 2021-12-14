from GGanalysislib.UpItem.UpItem import UpItem
import numpy as np

class Up4starWeapon(UpItem):
    # 对于UP四星进行了简化，忽略了五星及常驻四星对其的影响，造成计算概率略低
    def init_pity_p(self):
        self.pity_p = self.weapon_4star_pity()
    def set_const(self):
        # 保底参数
        self.pity_pos = 9           # 保底位置
        self.up_rate = 0.75         # UP概率
        self.up_type = 5            # UP物品数量

        # 普池默认参数 默认UP物品均不在普池
        self.want_in_stander = 0    # 想要的是否在常驻
        self.up_in_stander = 0      # UP物品在常驻池中的数量
        self.stander_num = 1        # 常驻池中物品数量


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    # 参数设定
    loc_get_item_num = 2
    loc_calc_pull = 40
    loc_pull_state = 0
    loc_up_guarantee = 0
    
    test_obj = Up4starWeapon
    dp_ans = test_obj.get_distribution(loc_get_item_num, loc_calc_pull, loc_pull_state, loc_up_guarantee)
    dp_ans = dp_ans.cumsum(axis=1)
    plt.plot(range(1, loc_calc_pull), dp_ans[loc_get_item_num][1:loc_calc_pull], color='red')
    
    test_time = 100000
    test_result = np.zeros(loc_calc_pull+1, dtype=float)
    for i in range(test_time):
        loc = test_obj.simulate_pull_stander(loc_pull_state, loc_calc_pull, loc_get_item_num)
        test_result[loc] += 1
    test_result /= test_result.sum()
    test_result = np.cumsum(test_result, axis=0) 
    plt.plot(range(1, loc_calc_pull), test_result[1:loc_calc_pull], color='blue')

    plt.show()