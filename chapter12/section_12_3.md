## 12.3 Matplotlib 数据可视化——一图胜千言

数据分析的最终目的是理解数据并传达洞察。一个精心设计的图表能在几秒内传达出表格需要几分钟才能表达的信息。Matplotlib 是 Python 可视化生态的根基——它模仿了 MATLAB 的绘图接口，提供了从简单折线图到复杂的 3D 图形的完整能力。

Matplotlib 有两种主要的绘图方式："pyplot 函数式 API"（快速、适合探索）和"面向对象 API"（灵活、适合定制）。本书以最常用的 pyplot 方式为主，同时会展示一些面向对象的示例。

### 12.3.1 安装与基本流程

```python
# pip install matplotlib
import matplotlib.pyplot as plt    # 社区约定

# 基本绘图流程——五步法
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.figure(figsize=(8, 5))         # 1. 创建画布（宽 8 英寸，高 5 英寸）
plt.plot(x, y, marker="o")         # 2. 绘制数据
plt.title("简单的折线图")           # 3. 设置标题
plt.xlabel("X 轴")                  # 4. 设置轴标签
plt.ylabel("Y 轴")
plt.grid(True)                      #   添加网格
plt.show()                          # 5. 显示图表

# 保存图片（替代 plt.show()）
# plt.savefig("chart.png", dpi=150, bbox_inches="tight")
```

### 12.3.2 折线图与散点图

```python
import matplotlib.pyplot as plt
import numpy as np

# 折线图——展示趋势
x = np.linspace(0, 10, 50)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.figure(figsize=(10, 5))
plt.plot(x, y_sin, label="sin(x)", color="blue", linewidth=2, linestyle="-")
plt.plot(x, y_cos, label="cos(x)", color="red", linewidth=2, linestyle="--")
plt.title("三角函数曲线")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper right")        # 显示图例
plt.axhline(y=0, color="gray", linewidth=0.5)    # 水平参考线
plt.grid(True, alpha=0.3)
plt.show()

# 散点图——展示两个变量之间的关系
np.random.seed(42)
x = np.random.randn(200)
y = x * 0.5 + np.random.randn(200) * 0.3     # y 与 x 正相关 + 噪声

plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.6, c=y, cmap="coolwarm", edgecolors="black", linewidth=0.5)
plt.title("散点图：两个变量的相关关系")
plt.xlabel("变量 X")
plt.ylabel("变量 Y")
plt.colorbar(label="Y 值")           # 颜色条
plt.show()
```

`scatter()` 的几个参数值得一提：
- `alpha` 控制透明度——点密集时可以防止"过度绘制"导致看不清分布
- `c` 和 `cmap` 结合可以让点的颜色表示第三个维度的信息
- `edgecolors` 给每个点添加边框，增强视觉辨识度

### 12.3.3 柱状图与直方图

```python
import matplotlib.pyplot as plt
import numpy as np

# 柱状图（Bar Chart）——比较分类数据
categories = ["语文", "数学", "英语", "物理", "化学"]
scores_stu_A = [85, 92, 78, 88, 90]
scores_stu_B = [78, 85, 90, 76, 82]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - width/2, scores_stu_A, width, label="学生A", color="#2196F3")
plt.bar(x + width/2, scores_stu_B, width, label="学生B", color="#FF9800")
plt.title("两名学生成绩对比")
plt.xlabel("科目")
plt.ylabel("分数")
plt.xticks(x, categories)            # 设置 X 轴刻度标签
plt.ylim(0, 100)                     # 设置 Y 轴范围
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.show()

# 水平柱状图——适合类别名较长的场景
products = ["智能手表 Pro Max", "无线蓝牙耳机", "便携充电宝", "机械键盘"]
sales = [1200, 3400, 2800, 1500]
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]

plt.figure(figsize=(10, 5))
plt.barh(products, sales, color=colors)
plt.title("各产品季度销量")
plt.xlabel("销量（件）")
plt.show()

# 直方图（Histogram）——展示数据分布
data = np.random.randn(10000)        # 10000 个标准正态分布数据

plt.figure(figsize=(10, 5))
plt.hist(data, bins=50, color="steelblue", edgecolor="white", alpha=0.8)
plt.title("标准正态分布直方图")
plt.xlabel("值")
plt.ylabel("频次")
plt.axvline(x=0, color="red", linestyle="--", label="均值")
plt.legend()
plt.show()
```

**柱状图 vs 直方图**——初学者常搞混：
- 柱状图（bar）：比较**分类数据**，每根柱子代表一个类别，柱子之间有间距
- 直方图（hist）：展示**连续数据的频率分布**，柱子紧挨在一起，宽度代表数据区间

### 12.3.4 饼图与箱线图

```python
import matplotlib.pyplot as plt

# 饼图——展示占比（适合 5-7 个类别以内）
labels = ["研发", "市场", "销售", "管理", "运维"]
sizes = [35, 25, 20, 12, 8]
explode = (0.05, 0, 0, 0, 0)         # 突出研发部门
colors = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0", "#607D8B"]

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=90, shadow=False)
plt.title("公司人员分布")
plt.axis("equal")                     # 确保饼图是正圆形
plt.show()

# 箱线图——展示数据的分布特征（中位数、四分位数、异常值）
np.random.seed(42)
data = [np.random.normal(70, 10, 100),    # 语文
        np.random.normal(65, 15, 100),    # 数学
        np.random.normal(75, 8, 100),     # 英语
        np.random.normal(60, 12, 100)]    # 物理

plt.figure(figsize=(10, 6))
bp = plt.boxplot(data, labels=["语文", "数学", "英语", "物理"],
                 patch_artist=True)
for patch, color in zip(bp["boxes"], ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0"]):
    patch.set_facecolor(color)
plt.title("各科成绩分布箱线图")
plt.ylabel("分数")
plt.grid(axis="y", alpha=0.3)
plt.show()
```

箱线图解读（自上而下）：
- 上须（upper whisker）：最大值（排除异常值后）
- 上四分位数（Q3）：75% 的数据小于这个值
- 中位数（median）：50% 的数据小于这个值
- 下四分位数（Q1）：25% 的数据小于这个值
- 下须（lower whisker）：最小值（排除异常值后）
- 圆点（异常值）：远高于上须或低于下须的极端值

### 12.3.5 多子图——一页多图

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))   # 2×2 子图网格

# 左上：折线图
axes[0, 0].plot(x, np.sin(x), color="blue")
axes[0, 0].set_title("sin(x)")
axes[0, 0].grid(True, alpha=0.3)

# 右上：散点图
np.random.seed(42)
axes[0, 1].scatter(np.random.randn(200), np.random.randn(200), alpha=0.5)
axes[0, 1].set_title("散点图")
axes[0, 1].grid(True, alpha=0.3)

# 左下：柱状图
axes[1, 0].bar(["A", "B", "C", "D"], [23, 45, 56, 78], color="orange")
axes[1, 0].set_title("柱状图")

# 右下：直方图
axes[1, 1].hist(np.random.randn(1000), bins=30, color="green", edgecolor="white")
axes[1, 1].set_title("直方图")

plt.tight_layout()                   # 自动调整子图间距
plt.show()
```

### 12.3.6 中文显示与样式美化

Matplotlib 默认不支持中文字体显示（会出现方块）。最简单的解决方案是设置支持中文的字体：

```python
import matplotlib.pyplot as plt
import platform

# 设置中文字体
if platform.system() == "Windows":
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
elif platform.system() == "Darwin":    # macOS
    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Heiti SC"]
else:                                  # Linux
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC"]

plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示为方块的问题

# 使用内置样式
print(plt.style.available[:5])         # 查看可用样式
plt.style.use("seaborn-v0_8-whitegrid")  # 应用样式——全局生效
```

### 12.3.7 实战练习

1. 创建一个 2×1 的子图布局（上下排列），上图绘制 2019-2023 年某公司的年收入折线图（数据自拟），下图绘制每年各季度的收入堆叠柱状图。

2. 生成 5000 个来自标准正态分布的随机数，绘制直方图（50 个 bins），在图上标注均值和 ±1 标准差的位置（用红色虚线）。

3. 读取一个 CSV 数据（或使用 Pandas 创建一个包含"城市""人口""GDP"三列的数据表），绘制一个散点图（X 轴=人口，Y 轴=GDP），点的大小与人口成正比，颜色与 GDP 成正比。添加数据标签和颜色条。