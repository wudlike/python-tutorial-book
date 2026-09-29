## 1.2 Python安装

Python 的安装流程因操作系统差异略有不同，但核心目标一致：配置一个稳定、可用的 Python 运行环境。本书推荐使用 **Python 3.10** 或更高版本，兼顾最新特性与第三方库兼容性。

本节分为两大部分：第一部分介绍 Windows、Ubuntu、macOS 三大平台的直接安装流程；第二部分说明为何**更推荐初学者使用 Anaconda**。若你已决定使用 Anaconda，可跳过本节直接阅读 1.3 节。

### 一、Windows 平台安装（Windows 10 / 11）

#### 1. 下载安装包

打开 Python 官方下载页面：[python.org/downloads/windows](https://www.python.org/downloads/windows/)，在"Stable Releases"区域选择对应系统的版本：

| 系统类型 | 选择 |
|:---------|:-----|
| 64 位（主流） | **Windows Installer (64-bit)** |
| 32 位（老旧设备） | Windows Installer (32-bit) |

> 如不确定系统位数，右键"此电脑" → "属性" → 查看"系统类型"。

#### 2. 安装配置

双击下载的 `.exe` 文件，**务必勾选"Add Python 3.12 to PATH"**——这是最关键的一步，决定了能否在命令行中直接使用 `python` 命令。建议选择"Install Now"使用默认配置即可。

#### 3. 验证安装

按下 `Win + R`，输入 `cmd` 打开命令提示符，依次执行：

```bash
# 查看Python版本
python --version # 或 python -V（大写V）
# 查看pip版本（包管理工具）
pip --version
```

若分别输出 `Python 3.12.x` 和 `pip 24.x` 的版本信息，说明安装成功。

\begin{warningbox}

**常见问题：提示"'python'不是内部或外部命令"**

这是因为安装时未勾选"Add Python to PATH"。解决方法：

1. 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
2. 在"用户变量"的 `Path` 中添加 Python 安装目录（如 `C:\Users\用户名\AppData\Local\Programs\Python\Python312`）和 Scripts 子目录（`...\Python312\Scripts`）
3. 重启命令提示符即可

\end{warningbox}

### 二、Ubuntu 平台安装（Ubuntu 20.04 / 22.04）

Ubuntu 默认预装 Python 3，但版本可能较旧。执行以下命令检查：

```bash
python3 --version
```

若显示 3.10 及以上，可直接使用；否则按以下步骤更新。

#### 1. 添加 Python 官方 PPA 源

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

#### 2. 安装 Python 3.12

```bash
sudo apt install python3.12 python3.12-pip python3.12-dev
```

其中 `python3.12-dev` 包含编译扩展所需的头文件，后续安装 NumPy 等库时依赖。

#### 3. 设为默认版本（可选）

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --config python3
```

选择 Python 3.12 对应的编号后回车。

#### 4. 验证

```bash
python3 --version
pip3 --version
```

### 三、macOS 平台安装（macOS 12+）

macOS 推荐通过 **Homebrew** 包管理器安装，兼顾便捷与版本管理。

#### 1. 安装 Homebrew（若未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

验证：`brew --version`。

#### 2. 通过 Homebrew 安装 Python

```bash
brew install python
```

Homebrew 会自动处理依赖，Python 将安装至 `/usr/local/Cellar/python/`（Intel 芯片）或 `/opt/homebrew/Cellar/python/`（M 系列芯片）。

#### 3. 配置环境变量

若 `python --version` 仍显示旧版 Python 2.7，需手动将 Homebrew 路径加入环境变量：

```bash
# Intel 芯片
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile && source ~/.bash_profile

# M系列芯片
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

#### 4. 验证

```bash
python --version
pip --version
```

### 四、跨平台通用验证

无论使用何种系统，安装完成后可通过安装一个第三方库来最终确认环境完整性，以numpy（常用科学计算库）为例：

```bash
# Windows / macOS
pip install numpy

# Ubuntu / Debian
pip3 install numpy
```

然后进入 Python 交互环境测试：

```python
import numpy as np
arr = np.array([1, 2, 3, 4])
print(arr)  # 输出: [1 2 3 4]
```

若能正常输出，说明 Python 环境已配置完毕。

\begin{tipbox}

**📦 更推荐：使用 Anaconda 一键安装**

如果你觉得上述步骤繁琐，或者担心后续管理多个项目时出现依赖冲突，我们强烈推荐使用 **Anaconda**。

Anaconda 是一套集成了 Python 解释器、包管理工具（conda）、环境管理工具和数百个常用科学计算库的完整生态系统。它能彻底解决以下痛点：

- 环境配置繁琐 → 一键安装即可使用
- 库安装冲突 → conda 自动处理依赖关系
- 多项目版本不兼容 → 虚拟环境互相隔离

关于 Anaconda 的详细安装与使用指南，请阅读下一节 **1.3 Anaconda 环境管理**。

\end{tipbox}

---

在完成 Python 环境的安装与验证之后，下一节我们将学习如何使用 Anaconda 进行更高效的环境管理——这是通往实战的第一步。