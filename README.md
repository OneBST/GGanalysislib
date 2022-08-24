# 原神抽卡概率分析工具包-GGanalysis

本工具包用于原神抽卡概率计算，~~且具备较高性能~~，目前大部分计算没有[GGanalysisLite](https://github.com/OneBST/GGanalysisLite)工具包快了，此工具包将仅仅进行简单的维护。

工具包默认采用的抽卡模型见[原神抽卡全机制总结](https://www.bilibili.com/read/cv10468091)

工具包绘制图表见[原神抽卡概率工具表](https://www.bilibili.com/read/cv12616453)，~~虽然这里面大部分图都该用GGanalysisLite绘制了~~。

样例程序为example.py，运行draw_img.py可以绘制出各种抽数分布图（常驻祈愿分布图绘制会比较慢）

### Python依赖及安装
#### Python依赖
1. numpy
2. matplotlib
#### 安装方式
1. 打开终端（Windows下可按快捷键`Win+r`后输入`cmd`并运行；macOS下按快捷键`command+空格`呼出spotlight，输入`terminal`或`终端（仅当系统语言为中文时）`后选择terminal.app）

2. 输入命令：

	```bash
	python3 -m pip install numpy matplotlib
	```

	\* Python路径可能根据个人电脑运行环境不同而变化；在Windows环境下，可能需要将Python添加到`PATH`环境变量中；在macOS及Linux环境下，请善用`which`命令确认当前使用的python路径

### 动态库编译说明

[GGanalysislib/bin](GGanalysislib/bin)下存放了工具包需要的动态链接库

在macOS上第一次使用时，需要在根目录下执行一次`make`以编译可用的二进制文件

如果你的mac上没有编译工具，可将[GGanalysislib/bin](GGanalysislib/bin)中的libGGanalysis.macos重命名并替换原有的libGGanalysis.so文件