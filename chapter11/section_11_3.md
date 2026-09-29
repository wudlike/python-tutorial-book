## 11.3 random/math 模块——随机与计算的基石

`random` 和 `math` 是每个 Python 程序员都会频繁接触的两个模块——前者提供随机数生成，后者提供数学函数和常量。它们看似简单，但随机数的"伪随机"本质、各种分布的采样策略、以及数学运算中的精度陷阱，都值得深入理解。

### 11.3.1 `random` 模块——可控的"不确定性"

Python 的 `random` 模块使用的是**伪随机数生成器**（PRNG，Pseudo-Random Number Generator）——它通过一个数学公式（默认为 Mersenne Twister 算法）从初始"种子"推导出看起来"随机"的数列。给定相同的种子，生成的随机数序列完全确定。这种"可复现"的特性对测试、模拟和游戏开发至关重要。

```python
import random

# 设置种子——相同种子 = 相同随机序列（对调试极其重要）
random.seed(42)
print(random.random())    # 0.6394267984578837
print(random.random())    # 0.025010755222666936

random.seed(42)            # 重置种子
print(random.random())    # 0.6394267984578837 —— 完全相同！
print(random.random())    # 0.025010755222666936 —— 完全相同！
```

#### 基础随机函数

```python
import random

# random() —— [0.0, 1.0) 之间的随机浮点数
print(random.random())                          # 0.6394...

# uniform(a, b) —— [a, b] 之间的随机浮点数
print(random.uniform(1, 10))                    # 7.231...

# randint(a, b) —— [a, b] 之间的随机整数（含两端）
print(random.randint(1, 6))                     # 模拟掷骰子

# randrange(start, stop[, step]) —— 从 range 中随机选一个
print(random.randrange(0, 101, 2))              # 0 到 100 之间的随机偶数

# choice(seq) —— 从序列中随机选一个元素
colors = ["红", "橙", "黄", "绿", "蓝", "靛", "紫"]
print(random.choice(colors))                    # 随机颜色

# choices(seq, weights, k) —— 带权重的多次抽样（可重复）
result = random.choices(["一等奖", "二等奖", "三等奖"],
                         weights=[1, 10, 89], k=3)
print(result)    # 如 ['三等奖', '三等奖', '二等奖']

# sample(seq, k) —— 不放回抽样 k 个（无重复）
lottery = random.sample(range(1, 50), k=6)
print(sorted(lottery))                          # 模拟彩票：6 个不重复的数字

# shuffle(seq) —— 原地打乱列表
cards = list(range(1, 53))                      # 52 张牌
random.shuffle(cards)
print(cards[:5])                                 # 发 5 张牌
```

`choices()` vs `sample()` 的关键区别：
- `choices()` 有放回——同一个元素可能被多次选中（适合模拟投骰子）
- `sample()` 不放回——每个元素最多被选中一次（适合抽签、洗牌）

#### 实用场景：随机数据生成

```python
import random
import string

def generate_password(length=12):
    """生成随机密码——包含大小写、数字和特殊字符"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choices(chars, k=length))

def generate_test_data(num_records=100):
    """生成测试数据——模拟用户表"""
    names = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]
    cities = ["北京", "上海", "广州", "深圳", "杭州"]

    records = []
    for _ in range(num_records):
        record = {
            "name": random.choice(names),
            "age": random.randint(18, 65),
            "city": random.choice(cities),
            "salary": round(random.uniform(5000, 50000), 2),
        }
        records.append(record)
    return records

print(generate_password(16))
# sample = generate_test_data(3)
# for r in sample:
#     print(r)
```

### 11.3.2 `math` 模块——精确的数学计算

`math` 模块提供了标准 C 库定义的数学函数。Python 内置的 `+` `-` `*` `/` `**` 已经覆盖了基础运算，所以 `math` 的真正价值在于**超越基本运算的数学需求**——三角函数、对数、取整、常量等：

```python
import math

# 常量和基础
print(f"π = {math.pi}")                          # 3.141592653589793
print(f"e = {math.e}")                            # 2.718281828459045
print(f"tau = {math.tau}")                        # 6.283185307179586（2π）

# 取整函数——四种不同的"整"
print(f"ceil(3.2)  = {math.ceil(3.2)}")           # 4 —— 向上取整
print(f"ceil(-3.2) = {math.ceil(-3.2)}")          # -3
print(f"floor(3.8) = {math.floor(3.8)}")          # 3 —— 向下取整
print(f"floor(-3.8)= {math.floor(-3.8)}")         # -4
print(f"trunc(3.8) = {math.trunc(3.8)}")          # 3 —— 向零取整（截断）
print(f"trunc(-3.8)= {math.trunc(-3.8)}")         # -3

# 对数
print(f"log(e)     = {math.log(math.e)}")          # 1.0 —— 自然对数（以 e 为底）
print(f"log2(8)    = {math.log2(8)}")              # 3.0
print(f"log10(1000)= {math.log10(1000)}")          # 3.0
print(f"log(8, 2)  = {math.log(8, 2)}")           # 3.0 —— 任意底数的对数

# 幂和根
print(f"sqrt(16)   = {math.sqrt(16)}")             # 4.0
print(f"pow(2, 10) = {math.pow(2, 10)}")          # 1024.0 —— 返回浮点数

# 三角函数（参数是弧度，不是角度）
angle_rad = math.radians(30)                       # 30° → 弧度
print(f"sin(30°)   = {math.sin(angle_rad)}")       # 0.5
print(f"cos(60°)   = {math.cos(math.radians(60))}") # 0.5

# 组合数学
print(f"阶乘 5!    = {math.factorial(5)}")         # 120
print(f"组合 C(5,2)= {math.comb(5, 2)}")          # 10 —— 5 选 2 的组合数
print(f"排列 P(5,2)= {math.perm(5, 2)}")          # 20 —— 5 选 2 的排列数

# 最大公约数 / 最小公倍数
print(f"gcd(48, 18) = {math.gcd(48, 18)}")        # 6
print(f"lcm(4, 6)   = {math.lcm(4, 6)}")          # 12（Python 3.9+）

# 判断
print(f"isclose(0.1+0.2, 0.3) = {math.isclose(0.1+0.2, 0.3)}")    # True
```

#### 浮点数精度——`0.1 + 0.2 != 0.3` 的真相

```python
print(0.1 + 0.2)             # 0.30000000000000004 —— 不是 0.3！

# 原因：0.1 和 0.2 在二进制中是无限循环小数，存储时被截断了
# 解决：用 math.isclose() 比较浮点数
print(math.isclose(0.1 + 0.2, 0.3))    # True

# 或者用 Decimal 做精确十进制运算
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2")) # 0.3 —— 精确！
```

### 11.3.3 两个模块的协同——模拟与统计

```python
import random
import math

def monte_carlo_pi(n=1_000_000):
    """蒙特卡洛法估算 π——随机投点"""
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:          # 点在单位圆内
            inside += 1
    return 4 * inside / n

random.seed(42)
estimate = monte_carlo_pi(1_000_000)
print(f"蒙特卡洛估算 π = {estimate:.6f}")      # 如 3.141600
print(f"math.pi      = {math.pi:.6f}")          # 3.141593
print(f"误差         = {abs(estimate - math.pi):.6f}")

def normal_random(mu=0, sigma=1, n=1000):
    """生成正态分布随机数——使用 Box-Muller 变换"""
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples

# 统计验证
samples = normal_random(n=10_000)
mean = sum(samples) / len(samples)
print(f"样本均值（应 ≈ 0）：{mean:.4f}")
```

### 11.3.4 实战练习

1. 编写一个"抽奖程序"——给定一个参与者列表，随机抽取 1 个一等奖、2 个二等奖、3 个三等奖，每人最多中奖一次。打印中奖名单。

2. 编写一个函数 `calc_triangle_area(a, b, angle_c)`，已知三角形两条边 `a`、`b` 及其夹角 `angle_c`（度数），计算三角形的面积。公式：`面积 = 0.5 * a * b * sin(夹角弧度)`。使用 `math` 模块。

3. 模拟抛硬币 10000 次，统计正面（1）和反面（0）各自出现的次数和比例。重复 1000 次这个实验，计算正面比例的均值和标准差。正面比例应该趋近于 0.5。