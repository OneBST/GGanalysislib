'''
    本例用于介绍GGanalysis工具包的简单使用方法
    by 一棵平衡树OneBST

    抽卡模型参数采用 https://www.bilibili.com/read/cv10468091
    四星的概率计算忽视了五星影响，UP四星忽视了四星的平稳机制，所得概率和理论值略微偏离，但偏离值可忽略
'''
import GGanalysislib

# 角色活动祈愿抽卡概率计算

player = GGanalysislib.Up5starCharacter()
print("抽90抽 能抽到 1个 UP五星角色的概率为")
print(player.get_p(1, 90))

# 对于更复杂的情况，可以指明垫抽数(pull_state参数) 和有无大保底情况(up_guarantee)
print("在有大保底，垫了 50抽 的情况下 抽120抽 能够抽到 2个 UP五星角色的概率为")
print(player.get_p(item_num=2, calc_pull=120, pull_state=50, up_guarantee=1))

# UP类型都有get_p函数
player = GGanalysislib.Up4starWeapon()
print("抽30抽 能抽到 1个 特定的UP四星武器的概率为")
print(player.get_p(1, 30))




# 武器活动祈愿抽卡概率计算

# 没有神铸定轨的武器活动祈愿，函数用法同其他UP池
player = GGanalysislib.Up5starWeaponOld()

# 带有神铸定轨的武器活动祈愿中，up_guarantee参数意义如下
# 0 表示上个五星抽到想要的UP        命定值为0
# 1 表示上个五星抽到不想要UP        命定值为1
# 2 表示上个五星抽到了常驻          命定值为1
# 3 表示，表示下个五星就是UP        命定值为2
player = GGanalysislib.Up5starWeaponEP()
print("命定值为1，上个五星抽到了常驻，垫了0抽的情况下，抽160抽能出指定一把UP武器的概率为")
print(player.get_p(item_num=1, calc_pull=160, pull_state=0, up_guarantee=1))




# 常驻祈愿抽卡概率计算

# 以常驻五星武器为例
player = GGanalysislib.Stander5StarWeapon()
print("常驻祈愿抽1000抽，抽到一把阿莫斯之弓的概率")
print(player.get_p(1, 1000))

# 由于常驻祈愿中平稳机制的影响稍大，可以手工设置平稳参数
player.last_type = 1            # 0表示上个五星是本类物品 1则表示异类物品
player.type_state = 100         # 多少抽没有另一类物品
print("常驻祈愿在100抽都没有五星武器的情况，距离上个五星已经抽了50抽的情况下，抽1000抽，抽到一把阿莫斯之弓的概率")
print(player.get_p(item_num=1, calc_pull=1000, pull_state=50))


# 欧气检测（适用于常驻祈愿和角色活动祈愿五星数的欧气检测，可图一乐）
player = GGanalysislib.PityGacha()
print("总共抽了100抽，出了2个五星，还垫了60抽")
print("你的运气击败了"+str(round(100*player.luck_evaluate(get_num=2, use_pull=100, left_pull=60), 2))+"%的玩家")

# 欧气检测（适用于角色活动祈愿UP五星数的欧气检测，可图一乐）
player = GGanalysislib.Up5starCharacter()
print("总共抽了100抽，出了1个UP五星，还垫了60抽, 有大保底")
print("你的运气击败了"+str(round(100*player.luck_evaluate(get_num=1, use_pull=100, left_pull=60, up_guarantee=1), 2))+"%的玩家")

# 其他复合情况
# 639抽抽到5个UP角色和1个定轨武器的概率是多少 注意这个没考虑策略，只是傻乎乎的抽到满足标准的概率
import numpy as np
use_pull = 639      # 用的抽数
character_num = 5   # 要抽的UP角色数量
weapon_num = 1      # 要抽的UP武器数量
test_obj = GGanalysislib.Up5starCharacter()
A = test_obj.get_distribution(character_num, character_num*180, 0 , 0)[character_num]
test_obj = GGanalysislib.Up5starWeaponEP()
B = test_obj.get_distribution(1, weapon_num*240, 0 , 0)[weapon_num]
C = np.convolve(A, B, mode='full')      # 卷积一下就得到了复合
print(sum(C[0:use_pull+1]))             # 输出概率


# 模型参数重设
'''
    计算工具默认采用 https://www.bilibili.com/read/cv10468091 中的模型，虽然效果已经非常好了，但不一定完全准确
    使用时可以手动设置模型参数，以获取采用其他参数的模型对应的概率
    只要也是抽卡概率随抽数上升机制的游戏，也可以直接套用本工具包进行抽卡概率的计算
'''
player = GGanalysislib.PityGacha()
# 设置为90抽保底
player.pity_pos = 90
import numpy as np
# 概率上升表数组大小至少为保底抽数+1
pity_p = np.ones(91, dtype=float)
pity_p *= 0.006
# 保底位置时概率必须设置为1
pity_p[90] = 1
# 设置修改后的模型
player.pity_p = pity_p

# 计算这一模型的基本统计量
player.init_item_statistics()
print("设置模型抽取物品期望抽数为"+str(round(player.item_expectation, 2)))