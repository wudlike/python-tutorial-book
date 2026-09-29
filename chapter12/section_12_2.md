## 12.2 Pandas 数据处理——表格数据的"瑞士军刀"

如果说 NumPy 处理的是"裸数值"，那 Pandas 处理的就是"带标签的结构化数据"——它把 Excel、SQL 和 NumPy 的核心思想融合在了一起。Pandas 的两个核心数据结构——**Series**（一维带标签数组）和 **DataFrame**（二维表格）——几乎可以表达你在真实世界中遇到的所有数据形式。

Pandas 的学习曲线比 NumPy 稍陡，因为它的 API 极其丰富（官方文档有 3000 多页）。但实际工作中你只需要掌握大约 20% 的功能就能处理 80% 的任务：读取数据、筛选、分组聚合、处理缺失值、合并、导出。

### 12.2.1 安装与导入

```python
# pip install pandas
import pandas as pd    # 社区约定别名
```

### 12.2.2 Series——带标签的一维数组

Series 可以理解为"NumPy 数组 + 索引标签"——每个数据点都有一个名字：

```python
import pandas as pd

# 从列表创建——默认索引是 0, 1, 2, ...
scores = pd.Series([85, 92, 78, 95])
print(scores)
# 0    85
# 1    92
# 2    78
# 3    95
# dtype: int64

# 自定义索引
scores = pd.Series([85, 92, 78, 95],
                   index=["数学", "语文", "英语", "编程"])
print(scores["语文"])                  # 92 —— 像字典一样用标签访问
print(scores[["数学", "编程"]])        # 多个标签一起查

# 向量化运算——和 NumPy 一样
print(scores.mean())                   # 87.5
print(scores[scores > 80])             # 筛选大于 80 的

# 从字典创建——键自动成为索引
fruit_prices = pd.Series({"苹果": 5.5, "香蕉": 3.2, "橘子": 4.0})
print(fruit_prices)
```

### 12.2.3 DataFrame——最核心的数据结构

DataFrame 是 Pandas 的灵魂——它像一个 Excel 表格或 SQL 表，有行索引和列名：

```python
import pandas as pd

# 从字典创建——键成为列名
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [25, 30, 22, 28],
    "城市": ["北京", "上海", "广州", "深圳"],
    "薪资": [15000, 20000, 12000, 18000],
}
df = pd.DataFrame(data)
print(df)
#    姓名  年龄  城市     薪资
# 0  张三  25  北京  15000
# 1  李四  30  上海  20000
# 2  王五  22  广州  12000
# 3  赵六  28  深圳  18000

# 基本属性
print(f"形状: {df.shape}")            # (4, 4)
print(f"列名: {df.columns.tolist()}")  # ['姓名', '年龄', '城市', '薪资']
print(f"数据类型:\n{df.dtypes}")
```

### 12.2.4 读取与写入——Pandas 支持几十种格式

```python
import pandas as pd

# CSV —— 最常用的数据交换格式
df = pd.read_csv("data.csv", encoding="utf-8")
df.to_csv("output.csv", index=False, encoding="utf-8")

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", sheet_name="结果", index=False)

# JSON
df = pd.read_json("data.json")
df.to_json("output.json", orient="records", force_ascii=False)

# SQL 数据库
# from sqlalchemy import create_engine
# engine = create_engine("sqlite:///database.db")
# df = pd.read_sql("SELECT * FROM users", engine)
# df.to_sql("users_backup", engine, if_exists="replace")

# 直接创建——方便演示和测试
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [25, 32, 28, 35],
    "salary": [50000, 65000, 55000, 80000],
    "department": ["研发", "市场", "研发", "管理"],
})
```

### 12.2.5 数据查看与筛选——"切片"表格

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 32, 28, 35, 23],
    "salary": [50000, 65000, 55000, 80000, 48000],
    "department": ["研发", "市场", "研发", "管理", "研发"],
})

# 查看头部/尾部
print(df.head(2))                    # 前 2 行
print(df.tail(1))                    # 后 1 行
print(df.sample(2))                  # 随机 2 行

# 基本信息——快速了解数据全貌
print(df.info())                     # 列类型、非空数量、内存占用
print(df.describe())                 # 数值列的统计摘要（均值、标准差、分位数等）

# 选择列
print(df["name"])                    # 单列 → Series
print(df[["name", "salary"]])        # 多列 → DataFrame

# loc —— 按标签索引
print(df.loc[0, "name"])             # 第 0 行 name 列
print(df.loc[1:3, ["name", "age"]])  # 第 1-3 行的 name 和 age 列

# iloc —— 按位置索引
print(df.iloc[0, 0])                 # 第 0 行第 0 列
print(df.iloc[:2, 1:3])              # 前 2 行，第 1-2 列

# 条件筛选——Pandas 最核心的查询方式
high_salary = df[df["salary"] > 55000]
print(high_salary)

rd_high = df[(df["department"] == "研发") & (df["salary"] > 50000)]
print(rd_high)

# query() —— SQL 风格的字符串查询
result = df.query("age >= 25 and department == '研发'")
print(result)

# isin() —— 值是否在列表中
target_depts = df[df["department"].isin(["研发", "管理"])]
print(target_depts)
```

### 12.2.6 数据处理——缺失值、排序、去重

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Bob"],
    "age": [25, np.nan, 28, 35, 32],
    "salary": [50000, 65000, np.nan, 80000, 65000],
})

# 缺失值处理
print(df.isnull())                   # 每个位置是否缺失（True/False）
print(df.isnull().sum())             # 每列缺失数量
df_dropped = df.dropna()             # 删除有缺失值的行
df_filled = df.fillna({"age": 0, "salary": df["salary"].median()})

# 排序
sorted_df = df.sort_values("salary", ascending=False)    # 按薪资降序
sorted_df = df.sort_values(["age", "salary"], ascending=[True, False])

# 去重
df_unique = df.drop_duplicates(subset=["name"])          # 按 name 去重，保留第一个
df_unique = df.drop_duplicates(subset=["name"], keep="last")  # 保留最后一个

# 重命名列
df_renamed = df.rename(columns={"name": "姓名", "age": "年龄", "salary": "薪资"})
```

### 12.2.7 分组聚合——Pandas 的"GROUP BY"

分组聚合是数据分析中最强大的操作之一——把数据按某个键分割成子集，对每个子集独立计算统计量，再把结果合并：

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "department": ["研发", "市场", "研发", "管理", "研发", "市场"],
    "salary": [50000, 65000, 55000, 80000, 60000, 70000],
    "age": [25, 32, 28, 35, 23, 30],
})

# 按部门分组，计算薪资的多种统计量
dept_stats = df.groupby("department")["salary"].agg(["count", "mean", "min", "max", "sum"])
print(dept_stats)

# 多列聚合——不同列用不同函数
stats = df.groupby("department").agg({
    "salary": ["mean", "max"],
    "age": ["mean", "min"],
})
print(stats)

# transform —— 保持原形状的聚合（用于计算"占比"等）
df["dept_avg"] = df.groupby("department")["salary"].transform("mean")
df["高出部门均薪"] = df["salary"] - df["dept_avg"]
print(df[["name", "department", "salary", "高出部门均薪"]])
```

### 12.2.8 数据合并——JOIN 操作

```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "dept_id": [10, 20, 10, 30],
})

departments = pd.DataFrame({
    "dept_id": [10, 20, 30],
    "dept_name": ["研发", "市场", "管理"],
})

# merge —— 类似 SQL JOIN
merged = pd.merge(employees, departments, on="dept_id", how="left")
print(merged)

# concat —— 纵向或横向拼接
more_employees = pd.DataFrame({
    "emp_id": [5, 6],
    "name": ["Eve", "Frank"],
    "dept_id": [20, 10],
})
all_employees = pd.concat([employees, more_employees], ignore_index=True)
print(all_employees)
```

### 12.2.9 实战练习

1. 读取一个 CSV 文件（如果手头没有，就自己创建一个包含"日期、产品、销量、单价"四列的模拟销售数据，至少 20 行），完成以下分析：
   - 计算每个产品的总销售额（销量 × 单价）
   - 找出销售额最高的 3 种产品
   - 按日期分组，计算每日总销售额

2. 处理一个包含缺失值的数据集——创建一个 DataFrame，在"年龄""薪资""部门"三列中各随机插入一些 `NaN`，然后：
   - 统计每列的缺失数量
   - 用该列的均值（数值列）或众数（分类列）填充缺失值
   - 验证填充后是否还有缺失值

3. 合并操作练习：创建"学生表"（学号、姓名、班级ID）和"班级表"（班级ID、班级名、班主任），使用 `merge` 操作得到每个学生的完整信息（含班级名和班主任）。