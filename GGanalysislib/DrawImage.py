import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties  # 字体管理器
import matplotlib.patheffects as pe
import matplotlib.cm as cm
import math

class DrawTransCDF():
    def get_tag(self, num):
        if self.item_type == "Character":
            return str(num-1) + '命'
        if self.item_type == "Type":
            if num == self.total_item_types:
                return '集齐'
            return str(num) + '种'
        if self.item_type == 'Weapon':
            return str(num) + '精'
        return 'TYPE SET ERROR!'

    def plot_img(self, cdf_ans):
        data_size = np.shape(cdf_ans)
        calc_pull = data_size[1]

        self.fig_size = [6, max(self.fig_size_y, math.log(calc_pull))]
        x_tick = 1/self.tick_number
        y_tick = self.tick_step*int(round(calc_pull/(self.tick_step*self.fig_size[1]/self.fig_size[0]*self.tick_number)))
        
        fig = plt.figure(dpi=self.img_dpi, figsize=self.fig_size) 
        ax = fig.gca()

        # 设置网格刻度和画图范围
        
        
        ax.set_xticks(np.arange(0, 1.01, x_tick))
        ax.set_yticks(np.arange(0, int(calc_pull/y_tick)*y_tick+1, y_tick))
        # The Ultimate Guide To Set Aspect Ratio in Matplotlib https://www.pythonpool.com/matplotlib-aspect-ratio/
        # ax.set_aspect((1.1/(calc_pull+y_tick))*((calc_pull+y_tick)/y_tick)/(1.1/x_tick)) # ((calc_pull+y_tick)/y_tick)/((1.1)/x_tick)
        
        plt.xlim(-0.05, 1.05)
        plt.ylim(-y_tick/2, calc_pull+y_tick/2)
        

        # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
        plt.grid(b=True, which='major', color='lightgray', linestyle='-', linewidth=1)
        plt.grid(b=True, which='minor', color='lightgray', linestyle='-', linewidth=0.5)
        plt.minorticks_on()  # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python

        # 设置字体偏置
        if self.open_mark_bias:
            x_bias = 1/self.bias_rate
            y_bias = calc_pull/self.bias_rate
        else:
            x_bias = 0
            y_bias = 0

        # 绘制图线
        for i in range(1, min(data_size[0], self.item_num+1)):
            plt.plot(   cdf_ans[i][1:calc_pull],
                        range(1, calc_pull),
                        # label='theory',
                        linewidth=2,
                        c=self.line_colors[i-1])
            for j in range(calc_pull):
                for each_pos in self.attention_pos:
                    if cdf_ans[i][j] >= each_pos >= cdf_ans[i][j-1]:
                        loc_x_bias = self.x_bias_num*x_bias
                        loc_y_bias = self.y_bias_num*y_bias
                        # 这里打的点实际上不是真的点，是为了图像好看而插值到直线上的
                        plt.scatter(each_pos, (each_pos-cdf_ans[i][j-1])/(cdf_ans[i][j]-cdf_ans[i][j-1])+j-1,
                                    color=self.line_colors[i-1],
                                    s=1,
                                    zorder=self.item_num+1,
                                    path_effects=[pe.withStroke(linewidth=2, foreground="white")])  
                        # 文字描边 https://stackoverflow.com/questions/25426599/matplotlib-how-to-buffer-label-text/25428107
                        # 官方文档 https://matplotlib.org/stable/tutorials/advanced/patheffects_guide.html
                        plt.text(each_pos+loc_x_bias, j+loc_y_bias, str(j),
                                fontproperties=self.text_font,
                                path_effects=[pe.withStroke(linewidth=self.font_stroke_width, foreground="white")])
                        # 标记%和对应竖虚线
                        if i == min(data_size[0], self.item_num+1)-1:
                            plt.plot([each_pos, each_pos], [-y_tick/2, j+y_tick*2], c='gray', linewidth=1.5, linestyle=':')
                            plt.text(each_pos-8*x_bias, j+y_tick*1.7, str(int(each_pos*100))+"%",
                                    c='gray',
                                    fontproperties=self.mark_font,
                                    path_effects=[pe.withStroke(linewidth=self.font_stroke_width, foreground="white")])
                        # 50%处标注说明文字
                        if each_pos == 0.5:
                            put_tag = self.get_tag(i)
                            plt.text(each_pos+loc_x_bias+self.mid_bias_num*x_bias, j+loc_y_bias, put_tag,
                                    c=self.line_colors[i-1],
                                    fontproperties=self.mark_font,
                                    path_effects=[pe.withStroke(linewidth=self.font_stroke_width, foreground="white")])
        plt.title(self.img_title, fontproperties=self.title_font)
        plt.xlabel("抽到概率", fontproperties=self.text_font)
        plt.ylabel("投入抽数", fontproperties=self.text_font)
        plt.text(0, calc_pull, self.img_description+"@一棵平衡树", c='#B0B0B0',
                fontproperties=self.mark_font,
                path_effects=[pe.withStroke(linewidth=self.font_stroke_width, foreground="white")],
                horizontalalignment='left',
                verticalalignment='top')
        if self.save_img:
            plt.savefig('./fig/'+self.img_name+'.png', bbox_inches='tight' , pad_inches=0.15)  # 
        if self.show_img:
            plt.show()

    def __init__(self):
        self.img_dpi = 100
        self.fig_size_y = 7
        self.back_line_color = "lightgray"
        self.attention_pos = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
        self.item_type = "Character"
        self.img_title = "Cumulative Distribution Function"
        self.img_name = "Cumulative Distribution Function"

        self.item_num = 7               # 绘制抽取物品数量 7时意味着 1100抽后才会开始自动延长
        self.total_item_types = 5       # 物品种类
        self.save_img = 0               # 是否保存图片
        self.show_img = 1               # 是否显示图片
        self.tick_step = 50             # y方向刻度对齐数值
        self.tick_number = 10           # x方向刻度个数
        # 字体偏移量及其它参数
        self.font_stroke_width = 1.5    # 字体描边大小
        self.open_mark_bias = 1         # 是否开启字体位置偏置
        self.bias_rate = 100            # 字体偏置比例
        self.x_bias_num = -5.8          # x方向偏移量
        self.y_bias_num = 0.5           # y方向偏移量
        self.mid_bias_num = -5.5        # 中部偏移量
        # 设置绘图字体
        self.text_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Medium.otf", size=10)
        self.title_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=15)
        self.mark_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=10)
        # 设置线条颜色
        # https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib
        self.line_colors = cm.Blues(np.linspace(0.5, 0.9, self.item_num))

        # 设置额外说明
        self.img_description = ''

if __name__ =='__main__':
    pass