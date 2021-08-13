# 原神抽卡概率分析工具包-GGanalysis

本工具包用于原神抽卡概率计算，且具备较高性能

工具包默认采用的抽卡模型见[原神抽卡全机制总结](https://www.bilibili.com/read/cv10468091)

工具包绘制图表见[原神抽卡概率工具表](https://www.bilibili.com/read/cv12616453)

样例程序为example.py

### 规划列表

- [ ] 将抽卡模拟器做的更易使用并合并到项目中
- [ ] 编写工具包函数说明
- [ ] 制作一个简易的图形界面
- [ ] 编写分析UP物品抽取运气的函数

### 动态库Linux编译说明

[GGanalysislib/bin](GGanalysislib/bin)下存放了工具包需要的动态链接库

- Windows下使用的GGanalysis.dll由MinGW编译，直接在根目录下make即可
- Linux下使用libGGanalysis.so，编译需将makefile.linux重命名为makefile，再在根目录使用gcc来make即可
- macOS下编译过程和Linux相同