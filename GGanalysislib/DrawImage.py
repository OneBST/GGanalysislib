import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties  # 字体管理器
import matplotlib.patheffects as pe
import matplotlib.cm as cm
import math

from numpy.core.fromnumeric import size

class DrawTransCDF():
    def get_tag(self, num):
        if self.item_type == 'NULL':  # 留空判定
                return '' 
        if self.en_switch:
            if self.item_type == "Character":
                return 'C' + str(num-1)
            if self.item_type == "Type":
                if num == self.total_item_types:
                    return 'ALL'
                return str(num)
            if self.item_type == 'Weapon':
                return 'R' + str(num) 
            return 'TYPE SET ERROR!'
        if self.item_type == "Character":
            return str(num-1) + '命'
        if self.item_type == "Type":
            if num == self.total_item_types:
                return '集齐'
            return str(num) + '种'
        if self.item_type == 'Weapon':
            return str(num) + '精'
        return 'TYPE SET ERROR!'

    def plot_img(self, cdf_ans, format='png'):
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
        plt.xlabel(self.xlabel, fontproperties=self.text_font)
        plt.ylabel(self.ylabel, fontproperties=self.text_font)
        plt.text(0, calc_pull, self.img_description+self.auther, c='#B0B0B0',
                fontproperties=self.mark_font,
                path_effects=[pe.withStroke(linewidth=self.font_stroke_width, foreground="white")],
                horizontalalignment='left',
                verticalalignment='top')
        if self.save_img:
            plt.savefig('./fig/'+self.img_name+'.'+format, bbox_inches='tight' , pad_inches=0.15)  # 
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
        # 设置图示语言
        self.en_switch = 0
        self.xlabel = "抽到概率"
        self.ylabel = "投入抽数"
        self.auther = "@一棵平衡树"
        # 设置线条颜色
        # https://stackoverflow.com/questions/12236566/setting-different-color-for-each-series-in-scatter-plot-on-matplotlib
        self.line_colors = cm.Blues(np.linspace(0.5, 0.9, self.item_num))

        # 设置额外说明
        self.img_description = ''

def plot_distribution(D, suptitle=None):
    # 输入的D为一维数组，从0开始
    end_pull = len(D)

    # 导入字体
    text_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Medium.otf", size=10)
    title_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=10)
    suptitle_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=15)
    mark_font = FontProperties(fname=r"./fonts/SourceHanSansSC-Bold.otf", size=10)
    
    # 自适应偏移量
    x_bias = end_pull / 100
    y_bias = 1/ 100

    # 绘图大小
    plt.figure(figsize=(9, 8))

    # 设置大图标题
    if suptitle != None:
        plt.suptitle(suptitle, fontproperties=suptitle_font)

    # 上图为累积分布函数
    plt.subplot(211)
    DD = D.cumsum()
    plt.plot(range(end_pull), DD)
    plt.title('累积分布函数', fontproperties=title_font)
    plt.xlabel('抽数', fontproperties=text_font)
    plt.ylabel('累积概率', fontproperties=text_font)
    attention_pos = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    for i in range(end_pull):   # 设置标记
        for each_pos in attention_pos:
            if DD[i] >= each_pos >= DD[i-1]:
                # 打点标记
                plt.scatter(i, DD[i], s=5, zorder=10, color='slateblue', 
                            path_effects=[pe.withStroke(linewidth=2, foreground="white")])  
                # 标记%和对应竖虚线
                plt.axvline(x=i, c="lightgray", ls="--", lw=1, zorder=0)
                plt.text(i+2.5*x_bias, each_pos-5*y_bias, str(i)+'抽  '+str(int(each_pos*100))+"%",
                        c='gray',
                        fontproperties=mark_font,
                        path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    # 下图为分布列
    plt.subplot(212)
    plt.plot(range(end_pull), D, c='salmon')
    plt.fill_between(range(end_pull), D, np.zeros(end_pull), alpha=0.2, color='salmon')
    plt.title('分布列', fontproperties=title_font)
    plt.xlabel('抽数', fontproperties=text_font)
    plt.ylabel('本抽概率', fontproperties=text_font)

    x0 = np.arange(end_pull)
    expectation = (x0*D).sum()
    # 标记期望和对应竖虚线
    plt.axvline(x=expectation, c="lightgray", ls="--", lw=1, zorder=0)
    plt.text(expectation+1*x_bias, D.max()/2, '期望:'+str(round(expectation, 2))+'抽',
            c='gray',
            fontproperties=mark_font,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")])
    # 标记分布峰值和对应竖虚线
    max_pos = D.argmax()
    y_pos_const = 0.75
    if (max_pos-expectation)/end_pull > 0.01:
        plt.axvline(x=max_pos, c="lightgray", ls="--", lw=1, zorder=0)
        y_pos_const = 0.5
    plt.text(max_pos+1*x_bias, y_pos_const*D.max(), '峰值:'+str(max_pos)+'抽',
            c='gray',
            fontproperties=mark_font,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")])
    plt.tight_layout()
    plt.show()
    


if __name__ =='__main__':
    pass