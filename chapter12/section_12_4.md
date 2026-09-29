## 12.4 实战案例：数据分析报告——从原始数据到洞察

前面的三节分别学习了 NumPy 的数组运算、Pandas 的数据处理和 Matplotlib 的可视化。这一节将三者串联起来，完成一个完整的"数据分析报告"流程：读取原始销售数据 → 清洗和转换 → 多维度聚合分析 → 可视化呈现 → 导出结论。这个工作流就是数据分析师日常工作的缩影。

### 12.4.1 场景设定

假设你是一家电子产品零售公司的数据分析师。公司给了你一份 2024 年上半年的销售记录（CSV 格式），你的任务是：分析销售趋势、找出明星产品和问题区域、生成一份图文并茂的分析报告。

### 12.4.2 第一步：读取与概览

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 模拟生成真实数据——涵盖不同产品、地区、时间
np.random.seed(42)
n = 500
dates = pd.date_range("2024-01-01", "2024-06-30", periods=n)
products = np.random.choice(["手机", "笔记本", "平板", "耳机", "手表"], n)
regions = np.random.choice(["华北", "华东", "华南", "西部"], n)

base_price = {"手机": 4000, "笔记本": 6000, "平板": 3000, "耳机": 500, "手表": 2000}
price = np.array([base_price[p] for p in products])
quantity = np.random.poisson(lam=3, size=n) + 1       # 每次购买 1-8 件
amount = price * quantity * np.random.uniform(0.85, 1.15, n)    # 加上折扣波动

df = pd.DataFrame({
    "日期": dates,
    "产品": products,
    "地区": regions,
    "单价": price,
    "销量": quantity,
    "金额": amount.round(2),
})

print("=" * 50)
print("数据概览")
print("=" * 50)
print(f"记录数: {len(df)}")
print(f"时间范围: {df['日期'].min().date()} ~ {df['日期'].max().date()}")
print(f"总销售额: {df['金额'].sum():,.0f} 元")
print(f"\n前 5 行:\n{df.head()}")
print(f"\n数据类型:\n{df.dtypes}")
```

### 12.4.3 第二步：数据清洗

真实数据总是不完美的。我们要检查缺失值、异常值、重复记录：

```python
print("=" * 50)
print("数据质量检查")
print("=" * 50)

print(f"缺失值:\n{df.isnull().sum()}")
print(f"\n重复行: {df.duplicated().sum()}")

# 检查异常值——金额为负或为 0
negative = df[df["金额"] <= 0]
if len(negative) > 0:
    print(f"\n异常金额记录: {len(negative)} 条")
    df = df[df["金额"] > 0]     # 剔除异常

# 检查异常值——销量异常大（超过该产品平均销量的 5 倍标准差）
for product in df["产品"].unique():
    subset = df[df["产品"] == product]
    mean = subset["销量"].mean()
    std = subset["销量"].std()
    outliers = subset[subset["销量"] > mean + 5 * std]
    if len(outliers) > 0:
        print(f"{product} 销量异常: {len(outliers)} 条（均值={mean:.1f}）")

# 提取月份——用于后续按月分析
df["月份"] = df["日期"].dt.month
print(f"\n清洗后记录数: {len(df)}")
```

### 12.4.4 第三步：多维度分析

从产品、地区、时间三个维度分析销售表现：

```python
print("\n" + "=" * 50)
print("多维度分析")
print("=" * 50)

# 按产品分析
product_stats = df.groupby("产品").agg(
    销售额=("金额", "sum"),
    销量=("销量", "sum"),
    订单数=("金额", "count"),
    均价=("单价", "mean"),
).sort_values("销售额", ascending=False)
product_stats["销售额占比"] = (product_stats["销售额"] / product_stats["销售额"].sum() * 100).round(1)
print(f"\n【按产品】\n{product_stats}")

# 按地区分析
region_stats = df.groupby("地区").agg(
    销售额=("金额", "sum"),
    订单数=("金额", "count"),
    客单价=("金额", "mean"),
).sort_values("销售额", ascending=False)
print(f"\n【按地区】\n{region_stats}")

# 按月趋势
monthly = df.groupby("月份")["金额"].sum()
print(f"\n【月度趋势】\n{monthly}")

# 产品×地区交叉——找出每个地区最畅销的产品
cross = df.groupby(["地区", "产品"])["金额"].sum().reset_index()
top_by_region = cross.loc[cross.groupby("地区")["金额"].idxmax()]
print(f"\n【各地区最畅销产品】\n{top_by_region.to_string(index=False)}")
```

### 12.4.5 第四步：可视化呈现

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 图 1：产品销售额对比（柱状图）
ax1 = axes[0, 0]
colors_bar = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0", "#F44336"]
bars = ax1.bar(product_stats.index, product_stats["销售额"] / 10000, color=colors_bar)
ax1.set_title("各产品销售额（万元）", fontsize=13, fontweight="bold")
ax1.set_ylabel("万元")
for bar, val in zip(bars, product_stats["销售额"] / 10000):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f"{val:.0f}", ha="center", fontsize=10)

# 图 2：月度销售趋势（折线图）
ax2 = axes[0, 1]
ax2.plot(monthly.index, monthly.values / 10000, marker="o",
         color="#2196F3", linewidth=2.5, markersize=8)
ax2.set_title("月度销售趋势（万元）", fontsize=13, fontweight="bold")
ax2.set_xlabel("月份")
ax2.set_ylabel("万元")
ax2.set_xticks(range(1, 7))
ax2.grid(True, alpha=0.3)

# 图 3：地区销售额占比（饼图）
ax3 = axes[1, 0]
wedges, texts, autotexts = ax3.pie(
    region_stats["销售额"], labels=region_stats.index,
    autopct="%1.1f%%", colors=["#2196F3", "#FF9800", "#4CAF50", "#9C27B0"],
    startangle=90, textprops={"fontsize": 11}
)
ax3.set_title("各地区销售额占比", fontsize=13, fontweight="bold")

# 图 4：产品×地区热力表（用气泡图近似）
ax4 = axes[1, 1]
for i, row in cross.iterrows():
    region_idx = list(region_stats.index).index(row["地区"])
    product_idx = list(product_stats.index).index(row["产品"])
    size = row["金额"] / 10000 * 15
    ax4.scatter(region_idx, product_idx, s=size, alpha=0.7,
                color=colors_bar[product_idx])
    if row["金额"] > cross["金额"].median():
        ax4.text(region_idx, product_idx, f"{row['金额']/10000:.0f}",
                 ha="center", va="center", fontsize=7)

ax4.set_xticks(range(len(region_stats.index)))
ax4.set_xticklabels(region_stats.index)
ax4.set_yticks(range(len(product_stats.index)))
ax4.set_yticklabels(product_stats.index)
ax4.set_title("产品×地区销售热力", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig("sales_report.png", dpi=150, bbox_inches="tight")
plt.show()
```

### 12.4.6 第五步：结论与洞察

从上述分析中，我们可以提炼出几点关键洞察（在你的报告中，这部分是分析价值最高的内容）：

```python
print("\n" + "=" * 50)
print("关键洞察")
print("=" * 50)

best_product = product_stats.index[0]
best_region = region_stats.index[0]
growth_rate = ((monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0] * 100)

print(f"1. 明星产品：{best_product}，贡献了 {product_stats.iloc[0]['销售额占比']}% 的销售额")
print(f"2. 核心市场：{best_region}，贡献了 {region_stats.iloc[0]['销售额'] / region_stats['销售额'].sum() * 100:.1f}% 的业绩")
print(f"3. 增长趋势：半年内月销售额增长 {growth_rate:.1f}%，呈{'上升' if growth_rate > 0 else '下降'}趋势")

worst = product_stats.index[-1]
print(f"4. 关注产品：{worst} 销售额最低，建议分析原因（定价？需求？竞争？）")

best_in_worst_region = cross[cross["地区"] == region_stats.index[-1]].nlargest(1, "金额")
print(f"5. 区域策略：{region_stats.index[-1]}区最畅销 {best_in_worst_region.iloc[0]['产品']}")

print(f"\n完整分析图表已保存至 sales_report.png")
```

### 12.4.7 这个案例教给你什么

1. **数据清洗占分析工作的 60-80%**——缺失值处理、异常值识别、格式统一，这些"脏活"决定了分析结果的可靠性
2. **多维度下钻**是发现洞察的核心方法——从整体到产品/地区/时间维度逐一拆解，总能发现被聚合数字掩盖的模式
3. **图表的选择**取决于你想传达的信息——对比用柱状图、趋势用折线图、占比用饼图、分布用直方图
4. **分析的终点是决策建议**——单纯列出数字没有价值，关键是"所以呢？接下来该做什么？"

### 12.4.8 实战练习

1. 基于本节的数据集，额外完成以下分析：
   - 计算每种产品在每个月的销量变化率（环比增长）
   - 找出每个地区客单价（平均每单金额）最高和最低的产品
   - 画一张 3×1 的图：上面是月度销量趋势，中间是产品月度堆叠面积图，下面是地区月度堆叠面积图

2. 在你的分析报告生成脚本中加入"自动导出 Excel"功能：将清洗后的数据、各维度统计表分别写入不同的 Sheet，同时将图表也嵌入 Excel 中（提示：使用 `pd.ExcelWriter` 和 `openpyxl`）。