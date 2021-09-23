'''
    原神抽卡概率计算工具包 GGanalysis
    by 一棵平衡树OneBST
    抽卡模型参数采用 https://www.bilibili.com/read/cv10468091
    神铸定轨对应翻译为 Epitomized Path https://www.hoyolab.com/genshin/article/533196
    四星的概率计算忽视了五星影响，UP四星忽视了四星的平稳机制，所得概率和理论值略微偏离，但偏离值可忽略
'''

from GGanalysislib.PityGacha import *

# 各类活动祈愿对应的类
from GGanalysislib.UpItem.Up5starCharacter import Up5starCharacter
from GGanalysislib.UpItem.Up4starCharacter import Up4starCharacter
from GGanalysislib.UpItem.Up5starWeaponOld import Up5starWeaponOld
from GGanalysislib.UpItem.Up5starWeaponEP import Up5starWeaponEP
from GGanalysislib.UpItem.Up4starWeapon import Up4starWeapon
# 常驻祈愿对应的类
from GGanalysislib.StanderItem.Stander5Star import Stander5StarCharacter
from GGanalysislib.StanderItem.Stander5Star import Stander5StarWeapon
from GGanalysislib.StanderItem.Stander4Star import Stander4StarCharacter
from GGanalysislib.StanderItem.Stander4Star import Stander4StarWeapon
# 绘图工具
from GGanalysislib.DrawImage import DrawTransCDF
from GGanalysislib.DrawImage import plot_distribution
# 概率分析工具
from GGanalysislib.PityCouplingP import calc_coupling_p
from GGanalysislib.PityCouplingP import calc_stationary_distribution

if __name__ == '__main__':
    pass