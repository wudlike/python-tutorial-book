## 12.1 NumPy 数组操作——Python 数值计算的基石

Python 的列表灵活通用，但处理大规模数值数据时有两个致命短板：速度慢、内存大。一个包含一百万个整数的 Python 列表，每个元素都是一个完整的 Python 对象（附带了引用计数、类型指针等开销），内存占用是原始数据的数倍。NumPy（Numerical Python）从根本上解决了这个问题——它使用**连续内存块**存储同类型数据，将循环运算下沉到 C 语言层面执行，性能和内存效率都提升了数十倍。

NumPy 是 Pandas、Matplotlib、SciPy、scikit-learn 等几乎所有 Python 数据科学库的底层依赖。即使你最终用 Pandas 做分析，理解 NumPy 的数组模型也能帮你写出更高效的代码。

### 12.1.1 安装与导入

```python
# 安装（在终端中执行）
# pip install numpy

import numpy as np    # 社区约定的别名，几乎所有 NumPy 代码都用 np
```

### 12.1.2 创建数组——`np.array()` 与快速生成函数

最基础的创建方式是把 Python 列表传给 `np.array()`：

```python
import numpy as np

# 从列表创建一维数组
arr1d = np.array([1, 2, 3, 4, 5])
print(arr1d)                      # [1 2 3 4 5]
print(type(arr1d))                # <class 'numpy.ndarray'>
print(arr1d.dtype)                # int32（取决于平台）

# 从嵌套列表创建二维数组（矩阵）
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

# 指定数据类型
arr_float = np.array([1, 2, 3], dtype=np.float64)
print(arr_float.dtype)            # float64
```

除了 `np.array()`，NumPy 提供了一系列快速生成函数——比用 Python 循环创建快几个数量级：

```python
import numpy as np

# 全零 / 全一数组
zeros = np.zeros((3, 4))          # 3 行 4 列的全零矩阵
ones = np.ones((2, 5))            # 2 行 5 列的全一矩阵

# 指定值的数组
full = np.full((3, 3), 7)         # 3×3 矩阵，全部填充 7

# 单位矩阵（对角线为 1，其余为 0）
identity = np.eye(4)              # 4×4 单位矩阵

# 等差数列
linear = np.arange(0, 10, 2)      # [0 2 4 6 8] —— 和 Python range 类似
linspace = np.linspace(0, 1, 5)   # [0.   0.25 0.5  0.75 1.  ] —— 均匀分割

# 随机数组
random_uniform = np.random.rand(3, 3)          # [0,1) 均匀分布
random_normal = np.random.randn(3, 3)           # 标准正态分布（均值 0，方差 1）
random_int = np.random.randint(0, 100, (3, 3))  # [0,100) 随机整数
```

### 12.1.3 数组属性——形状、维度、大小

```python
import numpy as np

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print(f"形状 (shape): {arr.shape}")          # (3, 4) —— 3 行 4 列
print(f"维度 (ndim):  {arr.ndim}")            # 2
print(f"元素总数 (size): {arr.size}")          # 12
print(f"数据类型 (dtype): {arr.dtype}")        # int32
print(f"每个元素的字节数: {arr.itemsize}")     # 4
print(f"总内存 (bytes): {arr.nbytes}")          # 48
```

### 12.1.4 索引与切片

NumPy 的切片和 Python 列表切片语法一致，但有一个关键差异：**NumPy 切片返回的是原数组的"视图"（view），而不是副本（copy）**。这意味着修改切片会影响原数组——这个特性可以避免不必要的内存拷贝，但也可能带来意料之外的副作用：

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# 基础索引——和列表一样
print(arr[0])                     # 10
print(arr[-1])                    # 50

# 切片——返回视图！
sub = arr[1:4]                    # [20 30 40]
sub[0] = 999                      # 修改 sub
print(arr)                        # [ 10 999  30  40  50] —— 原数组被改了！

# 如果确实需要副本，用 .copy()
sub_copy = arr[1:4].copy()
sub_copy[0] = 0
print(arr)                        # [ 10 999  30  40  50] —— 原数组不变

# 多维数组索引
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[0, 1])                # 2 —— 第 0 行第 1 列
print(arr2d[:, 1])                # [2 5 8] —— 所有行的第 1 列
print(arr2d[1:, :2])              # [[4 5] [7 8]] —— 第 1 行到末尾，前 2 列

# 布尔索引——按条件筛选
scores = np.array([85, 92, 78, 95, 60, 88])
print(scores[scores >= 90])       # [92 95] —— 大于等于 90 的分数
print(scores[(scores >= 60) & (scores < 80)])  # [78 60] —— 及格但未到良好

# 花式索引——用整数数组指定位置
print(scores[[0, 2, 4]])          # [85 78 60] —— 第 0、2、4 个元素
```

### 12.1.5 重塑与变形

```python
import numpy as np

arr = np.arange(12)               # [0 1 2 ... 11]

# reshape —— 改变形状（元素总数必须不变）
matrix = arr.reshape(3, 4)
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 多维 → 一维
flat = matrix.ravel()             # [0 1 2 ... 11] —— 展平（返回视图）
flat2 = matrix.flatten()          # 同上，但返回副本

# 转置
print(matrix.T)
# [[ 0  4  8]
#  [ 1  5  9]
#  [ 2  6 10]
#  [ 3  7 11]]

# 添加维度
arr_1d = np.array([1, 2, 3])
print(arr_1d[:, np.newaxis])      # 列向量 shape (3, 1)
print(arr_1d[np.newaxis, :])      # 行向量 shape (1, 3)

# 拼接
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
vstack = np.vstack([a, b])        # 垂直拼接
hstack = np.hstack([a, b.T])      # 水平拼接
```

### 12.1.6 向量化运算——NumPy 的核心优势

NumPy 最大的威力在于**向量化运算**（Vectorization）——直接用运算符对数组进行逐元素计算，无需写 `for` 循环：

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# 逐元素运算——一次搞定，底层是 C 循环
print(a + b)                      # [11 22 33 44 55]
print(a * b)                      # [10 40 90 160 250]
print(a ** 2)                     # [1 4 9 16 25]
print(np.sqrt(a))                 # [1. 1.414 1.732 2. 2.236]

# 广播机制——不同形状的数组也能运算
matrix = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3)
row = np.array([10, 20, 30])                  # shape (3,)
print(matrix + row)
# [[11 22 33]
#  [14 25 36]]  —— row 被"广播"到每一行

# 聚合函数——沿轴向缩减
scores = np.array([[85, 92, 78],
                   [76, 88, 95],
                   [90, 82, 87]])
print(f"全体平均: {scores.mean():.1f}")       # 85.9
print(f"每人平均: {scores.mean(axis=1)}")      # [85. 86.333 86.333] —— axis=1 沿列求平均（每行）
print(f"每科最高: {scores.max(axis=0)}")       # [90 92 95] —— axis=0 沿行求最大（每列）
print(f"总分: {scores.sum()}")                 # 773
print(f"标准差: {scores.std():.2f}")           # 6.17
```

NumPy 的 `where()` 函数提供了条件筛选的向量化版本——比布尔索引更灵活，类似于 Excel 的 `IF` 函数：

```python
import numpy as np

grades = np.array([85, 42, 78, 95, 60, 33, 88])
# 将不及格（<60）的替换为 60，其余保持不变
adjusted = np.where(grades < 60, 60, grades)
print(adjusted)    # [85 60 78 95 60 60 88]

# 分类——给分数打等级
levels = np.where(grades >= 90, "优秀",
         np.where(grades >= 75, "良好",
         np.where(grades >= 60, "及格", "不及格")))
print(levels)      # ['良好' '不及格' '良好' '优秀' '及格' '不及格' '良好']
```

### 12.1.7 线性代数基础

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法——用 @ 运算符（Python 3.5+）或 np.dot()
print(A @ B)                      # [[19 22] [43 50]]

# 逆矩阵
inv_A = np.linalg.inv(A)
print(inv_A)                      # [[-2.   1. ] [ 1.5 -0.5]]

# 验证：A @ inv_A = 单位矩阵
print(A @ inv_A)                  # [[1. 0.] [0. 1.]]

# 行列式
print(np.linalg.det(A))           # -2.0

# 特征值与特征向量
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"特征值: {eigenvalues}")
```

### 12.1.8 性能对比——为什么 NumPy 这么快

```python
import numpy as np
import time

n = 10_000_000

# Python 列表——慢
py_list = list(range(n))
start = time.perf_counter()
py_result = [x ** 2 for x in py_list]
print(f"Python 列表: {time.perf_counter() - start:.3f}s")

# NumPy 数组——快
np_arr = np.arange(n)
start = time.perf_counter()
np_result = np_arr ** 2
print(f"NumPy 数组:  {time.perf_counter() - start:.3f}s")
```

### 12.1.9 实战练习

1. 用 NumPy 创建一个 5×5 的随机整数矩阵（值在 10 到 100 之间），计算每一行的平均值和每一列的最大值。

2. 使用 NumPy 的向量化运算，计算从 1 加到 10000000 的平方和：`1² + 2² + 3² + ... + 10_000_000²`。对比使用 Python 原生循环的时间和 NumPy 的时间。

3. 给定一个学生成绩数组 `[78, 45, 92, 88, 55, 67, 95, 40, 73, 84]`，用 NumPy 完成以下操作：
   - 找出及格（≥60）的学生人数和比例
   - 将不及格的成绩替换为 60
   - 计算调整后的全班平均分