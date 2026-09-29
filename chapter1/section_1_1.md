## 1.1 为什么用Python——从小白到全球霸主的传奇

在开始编写第一行 Python 代码之前，我们先来回答一个根本性的问题：**为什么是 Python？** 放眼望去，编程语言成百上千，C、C++、Java、JavaScript、Go、Rust……每一门语言都有人在用，为什么 Python 会成为今天**全球最热门的编程语言**？

要理解这一点，我们需要从 Python 的源头讲起。

### Python 发展简史——一个圣诞节的礼物

\begin{tipbox}

**历史冷知识：** Python 的名字并非来自蟒蛇，而是源于 Guido van Rossum 最喜欢的英国喜剧团体 **Monty Python's Flying Circus（蒙提·派森的飞行马戏团）**。Guido 希望这门语言像马戏团的表演一样，有趣、灵活、让人愉快。

\end{tipbox}

#### Python 1.x 时代（1994—2000）：蹒跚起步

1989 年的圣诞节，荷兰程序员 **Guido van Rossum** 百无聊赖，决定写一个"消遣用的编程语言"。当时他在参与 ABC 语言的开发——ABC 是一门专为初学者设计的教学语言，语法非常优美，但性能太差、生态为零，最终失败了。

Guido 吸取了 ABC 的教训，把这个圣诞项目设计为：

- 像 ABC 一样**简洁易读**
- 能调用 C 语言库，**性能不拖后腿**
- 面向对象，但**不强制**

1991 年，第一个 Python 版本（0.9.0）发布。1994 年，Python 1.0 正式面世，带来了 `lambda`、`map`、`filter`、`reduce` 等函数式编程特性——这些特性至今仍是 Python 的标志。

\begin{definitionbox}

**Python 的设计哲学（Python之禅）**

1989 年，Guido 为 Python 确立了核心设计原则，后来被 Tim Peters 总结为《Python 之禅》。其中最重要的两条：

- **优美胜于丑陋（Beautiful is better than ugly.）**
- **简洁胜于复杂（Simple is better than complex.）**

在 Python 解释器中输入 `import this`，即可看到完整的 Python 之禅。

\end{definitionbox}

#### Python 2.x 时代（2000—2010）：生态大爆发

2000 年 10 月，Python 2.0 发布。这是 Python 历史上最重要的版本之一，带来了：

- **垃圾回收机制**（基于引用计数 + 循环检测）
- **Unicode 支持**（虽然还不完美）
- **列表推导式**（`[x for x in range(10)]`）
- **增强的异常处理**

这个时期，Python 的生态开始爆炸式增长。2003 年，**Django** 框架诞生；2005 年，**NumPy** 和 **SciPy** 让 Python 进入了科学计算领域；2008 年，**Python 3.0** 发布——但这是一个"不兼容"的版本，也是 Python 历史上最痛苦的阵痛期。

\begin{warningbox}

**Python 2 到 Python 3 的迁移之痛**

Python 3 修复了 Python 2 中大量历史遗留问题（最典型的是 `print` 从语句变成了函数），但这也意味着 **Python 2 的代码无法直接在 Python 3 上运行**。

这导致了一个长达 12 年的"双版本并行"期。直到 **2020 年 1 月 1 日**，Python 2.7 正式停止维护，Python 2 时代才真正画上句号。

**2025 年的今天，请不要再学 Python 2！** 本书所有内容基于 Python 3.10+。

\end{warningbox}

#### Python 3.x 时代（2008—至今）：AI 时代的王者

Python 3 的崛起，与四个关键趋势紧密相连：

1. **数据科学革命**（2012—）：Pandas、NumPy、Matplotlib 三大件让 Python 成为数据科学家的标配
2. **深度学习爆发**（2015—）：TensorFlow、PyTorch 全部选择 Python 作为首选语言
3. **大语言模型时代**（2022—）：GPT、LLaMA、Claude 等模型的训练和推理框架，**几乎全部用 Python 编写**
4. **教育普及**：全球高校纷纷将 Python 作为入门语言，取代了 Java 和 C++

\begin{notebox}

**震惊！这些改变世界的技术都是用 Python 写的**

| 技术 / 项目 | 领域 | Python 角色 |
|:-----------|:-----|:-----------|
| **ChatGPT / GPT-4** | 大语言模型 | PyTorch 训练 + 推理 |
| **AlphaGo / AlphaFold** | 强化学习 / 生物 | Python + TensorFlow |
| **TensorFlow / PyTorch** | 深度学习框架 | 核心 API 语言 |
| **Instagram（后端）** | 社交网络 | Django 框架 |
| **Spotify** | 音乐流媒体 | Python 后端服务 |
| **NASA** | 航天 | 科学计算脚本 |
| **Blender** | 3D 建模 | Python 脚本 API |

连 NASA 的火箭发射脚本都是用 Python 写的——还有什么理由不学？

\end{notebox}

### AI 时代的绝对霸主——用数据说话

如果说前面的介绍让你对 Python 有了感性的认识，那么下面这些**真实的数据**会让你彻底理解：为什么 Python 是这个时代不可撼动的王者。

#### 全领域渗透——Python 已成为智能时代的"操作系统"

Python 的触角早已伸向人类科技的最前沿。今天，无论你打开哪个领域的顶尖技术新闻，背后几乎都有 Python 的身影：

\begin{tipbox}

**🤖 Python 驱动的未来科技版图**

| 领域 | 典型应用 | Python 的角色 |
|:-----|:--------|:------------|
| 🧠 **大语言模型** | ChatGPT、GPT-4、LLaMA、Claude | PyTorch 训练 + 推理全流程 |
| 🚗 **自动驾驶** | Tesla Autopilot、Waymo | 感知算法、路径规划、仿真测试 |
| 🦾 **机器人** | Boston Dynamics、工业机器人 | ROS 控制、运动规划、SLAM |
| 🛸 **无人机** | 大疆、物流无人机 | 飞控算法、视觉导航、编队控制 |
| 🚀 **航空航天** | NASA、SpaceX | 轨道计算、遥测分析、发射脚本 |
| 🧬 **脑机接口** | Neuralink、脑科学研究 | 神经信号解码、实时数据处理 |
| 💰 **金融科技** | 量化交易、风控系统 | 策略回测、风险评估、高频交易 |
| 🔬 **生物医药** | AlphaFold、药物发现 | 蛋白质结构预测、基因分析 |

Python 已经成了**算法工程师的"第二母语"**，是他们每天打开电脑第一件事就会用到的思维工具。

\end{tipbox}

#### 市场份额——10 年数据告诉你谁是真正的王者

口说无凭，我们来看全球最权威的两大编程语言排行榜的数据。

根据 **TIOBE 编程社区指数 2026 年 9 月**的最新排名：

| 排名 | 语言 | 市场份额 | 同比变化 |
|:----:|:-----|:--------|:--------|
| 🥇 | **Python** | **17.76%** | 📉 -8.22% |
| 🥈 | C | 10.28% | 📈 +1.63% |
| 🥉 | C++ | 8.67% | → |
| 4 | Java | 7.54% | 📉 |
| 5 | C# | 4.22% | 📉 |
| 6 | JavaScript | 2.76% | 📉 |

根据 **PYPL 2026 年 1 月**榜单（基于 Google 教程搜索量）：

| 排名 | 语言 | 流行度 | 趋势 |
|:----:|:-----|:--------|:----:|
| 🥇 | **Python** | **24.61%** | 📉 -5.0% |
| 🥈 | Java | 14.72% | 📉 |
| 🥉 | JavaScript | 9.84% | → |
| 4 | C/C++ | 14.96% | 📈 +7.6% |
| 5 | C# | 6.83% | → |

> **数据来源说明：** TIOBE 数据来源为 [tiobe.com/tiobe-index](https://www.tiobe.com/tiobe-index) 2026年9月刊，PYPL 数据来源为 [pypl.github.io/PYPL.html](https://pypl.github.io/PYPL.html) 2026年1月刊。

两份权威排行榜一个共同的结论：**Python 虽然份额较 2025 年峰值有所回落，但仍以远超第二名的优势稳居全球第一**——在 TIOBE 上领先第二名 C 语言近 7.5 个百分点，在 PYPL 上更是以接近 10 个百分点的优势碾压 Java。

更震撼的是这张 10 年趋势图——Python 的崛起轨迹堪称"史诗级逆袭"：

![编程语言10年市场份额变迁](images/lang_market_share.png)

从图中可以清晰看到：2015 年 Python 还在 4% 左右徘徊，被 C 和 Java 远远甩在后面。之后的 10 年里，Java 和 C 稳步下滑，而 Python **一路狂飙**，在 2025 年达到惊人的 25.9% 峰值——超过了第二名到第五名的总和。2026 年虽有回落（这主要与 TIOBE 算法调整有关），但仍以 17.76% 的份额远超第二名。

\begin{definitionbox}

**为什么 Python 能持续正增长？**

其他顶级语言的衰退并非因为它们变差了，而是因为它们**生长的土壤在缩小**：

- **Java** 长期主导企业后端，但云原生和微服务时代，更轻量的 Go 和 Node.js 分流了大量用户
- **C / C++** 依然是系统编程的王者，但绝大多数新程序员不会从它们入门
- **JavaScript** 被浏览器牢牢绑定，跨不出前端

而 Python 恰恰相反——它生长的土壤是 **AI、数据科学、自动化、教育**，这四个领域过去 10 年在**爆炸性扩张**。Python 不是抢了谁的蛋糕，而是**在全新的领地上建立了帝国**。

\end{definitionbox}

### Python 与其他语言的对比——它凭什么"通杀"全球？

为了更直观地展示 Python 的地位，我们从三个维度来做对比。

#### 对比一：语法简洁度

用同一个功能——打印"Hello, World!"并计算 1 到 100 的和——来看看各语言需要多少代码：

```c
// C语言：需要管理内存、声明类型
#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        sum += i;
    }
    printf("Sum: %d\n", sum);
    return 0;
}
```

```cpp
// C++：同样的逻辑，更复杂的语法
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        sum += i;
    }
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
```

```java
// Java：必须定义类，啰嗦的 System.out
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        int sum = 0;
        for (int i = 1; i <= 100; i++) {
            sum += i;
        }
        System.out.println("Sum: " + sum);
    }
}
```

```python
# Python：几乎就是"伪代码"直接运行
print("Hello, World!")
print(f"Sum: {sum(range(1, 101))}")
```

**三行代码**就能完成 C 语言需要 10+ 行的逻辑。这就是 Python 的核心哲学：**代码是写给人看的，只是顺便让机器执行**。

\begin{tipbox}

**相同功能的代码行数对比：**

| 语言 | Hello World + 求和 | 跨平台 | 手动内存管理 |
|:-----|:------------------:|:------:|:-----------:|
| **Python** | **3 行** | ✅ | ❌ 不需要 |
| JavaScript | 4 行 | ✅ | ❌ 不需要 |
| Go | 12 行 | ✅ | ❌ 不需要 |
| Java | 10 行 | ✅ | ❌ 不需要 |
| C++ | 10 行 | ⚠️ 需编译 | ✅ 需要 |
| C | 11 行 | ⚠️ 需编译 | ✅ 需要 |

\end{tipbox}

#### 对比二：性能与生态

很多人会问：**Python 是不是很慢？** 这个问题不能简单地回答"是"或"否"。

| 维度 | C | C++ | Java | Python |
|:-----|:-:|:---:|:----:|:----------:|
| **原始执行速度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **开发速度** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **学习曲线** | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **AI / 数据科学** | ❌ | ⚠️ | ⚠️ | ⭐⭐⭐⭐⭐ |
| **Web 开发** | ❌ | ⚠️ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **跨平台** | ⚠️ | ⚠️ | ✅ | ✅ |
| **第三方库数量** | 少 | 中等 | 多 | **极其丰富（50万+）** |

\begin{definitionbox}

**Python 的"慢"到底慢在哪里？**

Python 是一门**解释型语言**：代码在运行时由解释器逐行翻译执行，而 C/C++ 是**编译型语言**，代码在运行前就被编译成了机器码。

但请注意——在 AI 和科学计算领域，Python 只是"指挥官"：

- **PyTorch / TensorFlow** 底层用 C++/CUDA 实现矩阵运算，Python 负责调度
- **NumPy** 的核心计算用 C 和 Fortran 实现，Python 负责组织逻辑

所以你写的 Python 代码只是**调度层**，真正的高强度计算全部发生在 C/C++ 层——**"慢"的是调度，快的在底层**。

\end{definitionbox}

#### 对比三：大语言模型时代——Python 的绝对统治

如果你对 AI 和大语言模型感兴趣，那么 Python 几乎是**必修课**。以下是 2025 年主流大模型框架的语言分布：

![Python在AI领域的统治地位](images/python_ai_dominance.png)

- **PyTorch**（Meta 出品）：Python 为核心 API 语言，底层 C++/CUDA
- **TensorFlow**（Google 出品）：Python 为主要前端语言
- **Hugging Face Transformers**：纯 Python 生态，10 万+ 预训练模型
- **LangChain / LlamaIndex**：大模型应用开发框架，100% Python

**一句话总结：不学 Python，等于自绝于 AI 时代。**

### Python 的核心优势总结

最后，我们用一张图来总结 Python 为什么能从一门"圣诞节消遣项目"成长为全球第一语言：

\begin{tipbox}

**🚀 Python 成功的四大支柱：**

1. **极简语法**：代码像伪代码一样可读，学习曲线极其平缓
2. **生态无敌**：PyPI 上超过 50 万个第三方包，覆盖一切你能想到的领域
3. **AI 时代的"普通话"**：从 PyTorch 到 LangChain，AI 世界的通用语言
4. **社区庞大**：全球最大的编程社区之一，任何问题都有人解决过

用 Guido van Rossum 自己的话说：

> "I was just trying to solve a problem for myself. I had no idea it would become this big."

他就是想给自己解决点小问题，没想到改变了整个世界。

\end{tipbox}

---

在了解了 Python 的传奇历史之后，下一节我们将动手**安装 Python 环境**——从零开始，让 Python 在你的电脑上跑起来。
