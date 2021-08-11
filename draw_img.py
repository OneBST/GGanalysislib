from typing import ItemsView
from GGanalysislib.UpItem.Up5starCharacter import Up5starCharacter
import GGanalysislib
import matplotlib.cm as cm
import numpy as np

# matplot colormap https://matplotlib.org/stable/tutorials/colors/colormaps.html
'''
# 角色活动祈愿五星角色
calc_obj = GGanalysislib.Up5starCharacter()
a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.Blues(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpCharacter5"
a.img_title = "原神UP五星角色抽取概率"
a.img_description = "获取一个物品的期望抽数为\n获取一个指定五星角色最多需要180抽\n"

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1150, 0).cumsum(axis=1))


# 角色活动祈愿四星角色
calc_obj = GGanalysislib.Up4starCharacter()
a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.Purples(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpCharacter4"
a.img_title = "原神三UP四星角色抽取特定角色概率"
a.img_description = "获取一个物品的期望抽数为\n无法保证在有限抽数内获得指定四星角色\n"

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 600, 0).cumsum(axis=1))


# 武器活动祈愿不定轨抽五星武器
calc_obj = GGanalysislib.Up5starWeaponOld()
a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
temp_color = np.ones((a.item_num, 4), dtype=float)/2
# a.line_colors = (temp_color+cm.Reds(np.linspace(0.5, 0.9, a.item_num)))/2
a.line_colors = (cm.Greys(np.linspace(0.5, 0.9, a.item_num))+cm.Reds(np.linspace(0.5, 0.9, a.item_num)))/2
# print(np.shape(a.line_colors))
a.img_name = "UpWeapon5Old"
a.img_title = "原神双UP五星武器不定轨抽取特定武器概率"
a.img_description = "获取一个物品的期望抽数为\n不定轨的情况下无法保证在有限抽数内获得指定武器\n"

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1600, 0).cumsum(axis=1))

# 武器活动祈愿定轨抽五星武器
calc_obj = GGanalysislib.Up5starWeaponEP()
a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.Reds(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpWeapon5EP"
a.img_title = "原神双UP五星武器定轨抽取特定武器概率"
a.img_description = "获取一个物品的期望抽数为\n定轨情况下获取一个指定五星武器最多需要240抽\n"

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1050, 0).cumsum(axis=1))


# 武器活动祈愿抽四星武器
calc_obj = GGanalysislib.Up4starWeapon()
a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.Oranges(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpWeapon4"
a.img_title = "原神五UP四星武器抽取特定武器概率"
a.img_description = "获取一个物品的期望抽数为\n无法保证在有限抽数内获得指定四星武器\n"

a.img_dpi = 100
a.save_img = 0               # 是否保存图片
a.show_img = 1               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 600, 0).cumsum(axis=1))


# 常驻祈愿抽五星角色
calc_obj = GGanalysislib.Stander5StarCharacter()
a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
a.img_name = "StanderCharacter5"
a.img_title = "原神常驻祈愿抽取特定五星角色概率"
a.img_description = "获取一个物品的期望抽数为"+str(round(calc_obj.item_expectation*calc_obj.stander_num, 2))+"抽\n无法保证在有限抽数内获得指定五星角色\n本图绘制时，常驻祈愿包含"+str(calc_obj.stander_num)+"种五星角色\n"
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 10100, 0).cumsum(axis=1))


# 常驻祈愿抽四星角色
calc_obj = GGanalysislib.Stander4StarCharacter()
a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.RdPu(np.linspace(0.5, 1, a.item_num))
a.img_name = "StanderCharacter4"
a.img_title = "原神常驻祈愿抽取特定四星角色概率"
a.img_description = "获取一个物品的期望抽数为"+str(round(calc_obj.item_expectation*calc_obj.stander_num, 2))+"抽\n无法保证在有限抽数内获得指定四星角色\n本图绘制时，常驻祈愿包含"+str(calc_obj.stander_num)+"种四星角色\n"
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = 300
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 5000, 0).cumsum(axis=1))
'''

# 常驻祈愿抽五星武器
# calc_obj = GGanalysislib.Stander5StarWeapon()
# a = GGanalysislib.DrawTransCDF()
# a.item_num = 5
# a.item_type = "Weapon"
# a.line_colors = cm.OrRd(np.linspace(0.4, 1, a.item_num))
# a.img_name = "StanderWeapon5"
# a.img_title = "原神常驻祈愿抽取特定五星武器概率"
# a.img_description = "获取一个物品的期望抽数为"+str(round(calc_obj.item_expectation*calc_obj.stander_num, 2))+"抽\n无法保证在有限抽数内获得指定五星武器\n本图绘制时，常驻祈愿包含"+str(calc_obj.stander_num)+"种五星武器\n"
# a.x_bias_num = -7.6          # x方向偏移量

# a.img_dpi = 300
# a.save_img = 1               # 是否保存图片
# a.show_img = 0               # 是否显示图片
# a.plot_img(calc_obj.get_distribution(a.item_num, 16000, 0).cumsum(axis=1))

# 常驻祈愿抽四星武器
# calc_obj = GGanalysislib.Stander4StarWeapon()
# a = GGanalysislib.DrawTransCDF()
# a.item_num = 5
# a.item_type = "Weapon"
# a.line_colors = cm.YlOrRd(np.linspace(0.3, 1, a.item_num))
# a.img_name = "StanderWeapon4"
# a.img_title = "原神常驻祈愿抽取特定四星武器概率"
# a.img_description = "获取一个物品的期望抽数为"+str(round(calc_obj.item_expectation*calc_obj.stander_num, 2))+"抽\n无法保证在有限抽数内获得指定四星武器\n本图绘制时，常驻祈愿包含"+str(calc_obj.stander_num)+"种四星武器\n"
# a.x_bias_num = -7.6          # x方向偏移量

# a.img_dpi = 300
# a.save_img = 1               # 是否保存图片
# a.show_img = 0               # 是否显示图片
# a.plot_img(calc_obj.get_distribution(a.item_num, 3900, 0).cumsum(axis=1))


# 常驻祈愿抽齐五星角色
# calc_obj = GGanalysislib.Stander5StarCharacter()
# calc_obj.collect_all = 1
# a = GGanalysislib.DrawTransCDF()
# a.item_num = 5
# a.item_type = "Type"
# a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
# a.img_name = "GetAllStanderCharacter5"
# a.img_title = "原神集齐常驻祈愿五星角色概率"

# a.img_description = "集齐物品的期望抽数为"+"抽\n无法保证在有限抽数集齐常驻祈愿五星角色\n"
# a.x_bias_num = -7.6          # x方向偏移量

# a.img_dpi = 100
# a.save_img = 0               # 是否保存图片
# a.show_img = 1               # 是否显示图片
# a.plot_img(calc_obj.get_distribution(a.item_num, 4100, 0).cumsum(axis=1))

# 常驻祈愿抽齐四星角色
calc_obj = GGanalysislib.Stander4StarCharacter()
calc_obj.collect_all = 1
a = GGanalysislib.DrawTransCDF()
a.item_num = 18
a.total_item_types = 18       # 物品种类
a.fig_size_y = 20
a.item_type = "Type"
a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
a.img_name = "GetAllStanderCharacter4"
a.img_title = "原神集齐常驻祈愿四星角色概率"

a.img_description = "集齐物品的期望抽数为"+"抽\n无法保证在有限抽数集齐常驻祈愿四星角色\n"
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = 100
a.save_img = 1               # 是否保存图片
a.show_img = 0               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 2400, 0).cumsum(axis=1))

# 常驻祈愿抽齐五星武器
# calc_obj = GGanalysislib.Stander5StarWeapon()
# calc_obj.collect_all = 1
# a = GGanalysislib.DrawTransCDF()
# a.item_num = 10
# a.total_item_types = 10       # 物品种类
# a.item_type = "Type"
# a.fig_size_y = 12
# a.line_colors = cm.OrRd(np.linspace(0.4, 1, a.item_num))
# a.img_name = "GetAllStanderWeapon5"
# a.img_title = "原神集齐常驻祈愿五星武器概率"
# a.img_description = "集齐物品的期望抽数为"+"抽\n无法保证在有限抽数集齐常驻祈愿五星角色\n"
# a.x_bias_num = -7.6          # x方向偏移量

# a.img_dpi = 300
# a.save_img = 1               # 是否保存图片
# a.show_img = 0               # 是否显示图片
# a.plot_img(calc_obj.get_distribution(a.item_num, 9500, 0).cumsum(axis=1))