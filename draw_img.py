from GGanalysislib.UpItem.Up5starCharacter import Up5starCharacter
import GGanalysislib
import matplotlib.cm as cm
import numpy as np

# matplot colormap https://matplotlib.org/stable/tutorials/colors/colormaps.html

img_dpi = 300
save_img = 1
show_img = 0
en_switch = 0

a = GGanalysislib.DrawTransCDF()

text_model = "采用bilibili.com/read/cv10468091模型\n"
if en_switch:
    text_model = "Gacha model is from www.bilibili.com/read/cv10468091\n"
    a.xlabel = "Probability"
    a.ylabel = "Wishes"
    a.auther = "@一棵平衡树OneBST"
    a.en_switch = 1
    from matplotlib.font_manager import FontProperties  # 字体管理器
    a.mark_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=8)

# 角色活动祈愿五星角色
calc_obj = GGanalysislib.Up5starCharacter()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.Blues(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpCharacter5"
a.img_title = "原神UP五星角色抽取概率"
text_note = "本算例中UP物品均不在常驻祈愿中\n"
text_up_expectation = "获取一个特定UP物品的期望为"+str(round(calc_obj.reference_upitem_expectation,2))+"抽\n"
text_up_badcase = "获取一个特定UP物品最多需要"+str(2*calc_obj.pity_pos)+"抽\n"

if en_switch:
    a.img_title = "Probability of getting rate up 5* character\nin character event wish"
    text_note = "Suppose none of the rate up items are in permanent wish\n"
    text_up_expectation = "The expected wishes of obtaining one specific rate up item is "+str(round(calc_obj.reference_upitem_expectation,2))+"\n"
    text_up_badcase = "You need at most "+str(2*calc_obj.pity_pos)+" wishes to get one specific rate up item\n"

a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1150, 0).cumsum(axis=1))


# 角色活动祈愿四星角色
calc_obj = GGanalysislib.Up4starCharacter()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.Purples(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpCharacter4"
a.img_title = "原神三UP四星角色抽取特定角色概率"

text_note = "本算例中UP物品均不在常驻祈愿中\n绘图曲线忽略五星与四星耦合情况\n"

temp_obj = GGanalysislib.PityGacha()
# print(type(temp_obj.weapon_4star_pity()))
coupling_4star_p = GGanalysislib.calc_coupling_p(temp_obj.common_5star_pity(), temp_obj.common_4star_pity())
up_multi = (2-calc_obj.up_rate) * calc_obj.up_type
text_up_expectation = "考虑耦合时获取一个特定UP物品的期望为"+str(round(up_multi/coupling_4star_p,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
if en_switch:
    a.img_title = "Probability of getting rate up 4* character\nin character event wish"
    text_note = "Suppose none of the rate up items are in permanent wish\n"
    text_up_expectation = "The expected wishes of obtaining one specific rate up item is "+str(round(up_multi/coupling_4star_p,2))+"\n"
    text_up_badcase = "*Attention\nCan't guarantee that certain items will be obtained within limited wishes\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 600, 0).cumsum(axis=1))


# 武器活动祈愿不定轨抽五星武器
calc_obj = GGanalysislib.Up5starWeaponOld()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
temp_color = np.ones((a.item_num, 4), dtype=float)/2
# a.line_colors = (temp_color+cm.Reds(np.linspace(0.5, 0.9, a.item_num)))/2
a.line_colors = (cm.Greys(np.linspace(0.5, 0.9, a.item_num))+cm.Reds(np.linspace(0.5, 0.9, a.item_num)))/2
# print(np.shape(a.line_colors))
a.img_name = "UpWeapon5Old"
a.img_title = "原神双UP五星武器不定轨抽取特定武器概率"

text_note = "本算例中UP物品均不在常驻祈愿中\n"
text_up_expectation = "获取一个特定UP物品的期望为"+str(round(calc_obj.reference_upitem_expectation,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
if en_switch:
    a.img_title = "Probability of getting rate up 5* weapon\n(without Epitomized Path)"
    text_note = "Suppose none of the rate up items are in permanent wish\n"
    text_up_expectation = "The expected wishes of obtaining one specific rate up item is "+str(round(calc_obj.reference_upitem_expectation,2))+"\n"
    text_up_badcase = "*Attention\nCan't guarantee that certain items will be obtained within limited wishes\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1600, 0).cumsum(axis=1))

# 武器活动祈愿定轨抽五星武器
calc_obj = GGanalysislib.Up5starWeaponEP()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.Reds(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpWeapon5EP"
a.img_title = "原神双UP五星武器定轨抽取特定武器概率"

text_note = "本算例中UP物品均不在常驻祈愿中\n"
text_up_expectation = "获取一个特定UP物品的期望为"+str(round(calc_obj.reference_upitem_expectation,2))+"抽\n"
text_up_badcase = "获取一个特定UP物品最多需要"+str(3*calc_obj.pity_pos)+"抽\n"
if en_switch:
    a.img_title = "Probability of getting rate up 5* weapon\n(with Epitomized Path)"
    text_note = "Suppose none of the rate up items are in permanent wish\n"
    text_up_expectation = "The expected wishes of obtaining one specific rate up item is "+str(round(calc_obj.reference_upitem_expectation,2))+"\n"
    text_up_badcase = "You need at most "+str(3*calc_obj.pity_pos)+" wishes to get one specific rate up item\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1050, 0).cumsum(axis=1))


# 武器活动祈愿抽四星武器
calc_obj = GGanalysislib.Up4starWeapon()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.Oranges(np.linspace(0.5, 0.9, a.item_num))
a.img_name = "UpWeapon4"
a.img_title = "原神五UP四星武器抽取特定武器概率"

text_note = "本算例中UP物品均不在常驻祈愿中\n绘图曲线忽略五星与四星耦合情况\n"
temp_obj = GGanalysislib.PityGacha()
up_multi = (2-calc_obj.up_rate) * calc_obj.up_type
coupling_4star_p = GGanalysislib.calc_coupling_p(temp_obj.weapon_5star_pity(), temp_obj.weapon_4star_pity())
text_up_expectation = "考虑耦合时获取一个特定UP物品的期望为"+str(round(up_multi/coupling_4star_p,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
if en_switch:
    a.img_title = "Probability of getting rate up 4* weapon\nin weapon event wish"
    text_note = "Suppose none of the rate up items are in permanent wish\n"
    text_up_expectation = "The expected wishes of obtaining one specific rate up item is "+str(round(up_multi/coupling_4star_p,2))+"\n"
    text_up_badcase = "*Attention\nCan't guarantee that certain items will be obtained within limited wishes\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 600, 0).cumsum(axis=1))



'''
# 常驻祈愿抽五星角色
calc_obj = GGanalysislib.Stander5StarCharacter()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
a.img_name = "StanderCharacter5"
a.img_title = "原神常驻祈愿抽取特定五星角色概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种五星角色\n"
temp_obj = GGanalysislib.PityGacha()
text_up_expectation = "获取一个五星物品的期望为"+str(round(calc_obj.item_expectation,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 10100, 0).cumsum(axis=1))


# 常驻祈愿抽四星角色
calc_obj = GGanalysislib.Stander4StarCharacter()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 7
a.item_type = "Character"
a.line_colors = cm.RdPu(np.linspace(0.5, 1, a.item_num))
a.img_name = "StanderCharacter4"
a.img_title = "原神常驻祈愿抽取特定四星角色概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种四星角色\n"
temp_obj = GGanalysislib.PityGacha()
coupling_4star_p = GGanalysislib.calc_coupling_p(temp_obj.weapon_5star_pity(), temp_obj.weapon_4star_pity())
text_up_expectation = "获取一个四星物品的期望为"+str(round(1/coupling_4star_p,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase

a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 5000, 0).cumsum(axis=1))


# 常驻祈愿抽五星武器
calc_obj = GGanalysislib.Stander5StarWeapon()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.OrRd(np.linspace(0.4, 1, a.item_num))
a.img_name = "StanderWeapon5"
a.img_title = "原神常驻祈愿抽取特定五星武器概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种五星武器\n"
temp_obj = GGanalysislib.PityGacha()
text_up_expectation = "获取一个五星物品的期望为"+str(round(calc_obj.item_expectation,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 16000, 0).cumsum(axis=1))


# 常驻祈愿抽四星武器
calc_obj = GGanalysislib.Stander4StarWeapon()
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Weapon"
a.line_colors = cm.YlOrRd(np.linspace(0.3, 1, a.item_num))
a.img_name = "StanderWeapon4"
a.img_title = "原神常驻祈愿抽取特定四星武器概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种四星武器\n"
temp_obj = GGanalysislib.PityGacha()
coupling_4star_p = GGanalysislib.calc_coupling_p(temp_obj.weapon_5star_pity(), temp_obj.weapon_4star_pity())
text_up_expectation = "获取一个四星物品的期望为"+str(round(1/coupling_4star_p,2))+"抽\n"
text_up_badcase = "无法保证在有限抽数内必能获得特定物品\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 3900, 0).cumsum(axis=1))


# 常驻祈愿抽齐五星角色
calc_obj = GGanalysislib.Stander5StarCharacter()
calc_obj.collect_all = 1
# a = GGanalysislib.DrawTransCDF()
a.item_num = 5
a.item_type = "Type"
a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
a.img_name = "GetAllStanderCharacter5"
a.img_title = "原神集齐常驻祈愿五星角色概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种五星角色\n"
text_up_expectation = ""
text_up_badcase = "无法保证在有限抽数内必能集齐\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量
a.mid_bias_num = -7

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 4100, 0).cumsum(axis=1))

# 常驻祈愿抽齐五星武器
calc_obj = GGanalysislib.Stander5StarWeapon()
calc_obj.collect_all = 1
# a = GGanalysislib.DrawTransCDF()
a.item_num = 10
a.total_item_types = 10       # 物品种类
a.item_type = "Type"
a.fig_size_y = 12
a.line_colors = cm.OrRd(np.linspace(0.4, 1, a.item_num))
a.img_name = "GetAllStanderWeapon5"
a.img_title = "原神集齐常驻祈愿五星武器概率"

text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种五星武器\n"
text_up_expectation = ""
text_up_badcase = "无法保证在有限抽数内必能集齐\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量
a.mid_bias_num = -7

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 9500, 0).cumsum(axis=1))

# 常驻祈愿抽齐某类四星
from GGanalysislib.StanderItem.Stander4Star import Stander4Star
calc_obj = Stander4Star()
calc_obj.collect_all = 1
calc_obj.stander_num = 18     # 计算时物品种类
# a = GGanalysislib.DrawTransCDF()
a.item_num = 18
a.total_item_types = 18       # 画图物品种类
a.fig_size_y = 20
a.item_type = "Type"
a.line_colors = cm.PuRd(np.linspace(0.5, 1, a.item_num))
a.img_name = "GetAllStander4"
a.img_title = "原神集齐常驻祈愿某类四星概率"


text_note = "本算例中常驻祈愿中有"+str(calc_obj.stander_num)+"种本类物品\n"
text_up_expectation = ""
text_up_badcase = "无法保证在有限抽数内必能集齐\n"
a.img_description = text_model+text_note+text_up_expectation+text_up_badcase
a.x_bias_num = -7.6          # x方向偏移量
a.y_bias_num = 0.2
a.mid_bias_num = -7

a.img_dpi = img_dpi
a.save_img = save_img               # 是否保存图片
a.show_img = show_img               # 是否显示图片
a.plot_img(calc_obj.get_distribution(a.item_num, 1500, 0).cumsum(axis=1))
'''