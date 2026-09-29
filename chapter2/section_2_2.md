## 2.2 编辑器安装——VS Code

写 Python 代码，理论上用记事本就够了——但"够用"和"好用"之间，隔着巨大的效率鸿沟。一款好的代码编辑器，能帮你自动补全代码、高亮语法、快速定位错误，把精力真正花在"思考逻辑"上，而不是"找拼写错误"。

在众多编辑器中，本书推荐 **Visual Studio Code（简称 VS Code）**——微软出品的免费、开源、跨平台编辑器，装机量全球第一，也是算法工程师和数据科学家使用最广泛的开发工具。

### 主流编辑器对比

在决定使用 VS Code 之前，先了解市场上几款主流工具各自的特点，有助于你根据自身情况做出选择：

| 编辑器 | 定位 | 优点 | 缺点 | 适合人群 |
|:-------|:-----|:-----|:-----|:---------|
| **IDLE** | Python 自带 | 零配置，随 Python 自动附带 | 功能简陋，无智能提示，不支持多文件管理 | 仅写单文件简单代码的绝对新手 |
| **PyCharm** | 专业 Python IDE | 智能提示极强，内置调试/测试/项目管理 | 体积大（1 GB+），启动慢，免费版功能有限 | 长期深耕 Python 项目开发 |
| **Sublime Text** | 轻量高速编辑器 | 启动极快，内存占用少，插件丰富 | 免费版有弹窗提示，Python 调试需手动配置插件 | 追求速度的轻量编程 |
| **VS Code** | 轻量免费 + 插件化 | 启动快、免费开源、插件生态完善、可兼顾多语言 | 默认不支持 Python，需手动装插件 | **本书推荐首选** |

\begin{definitionbox}

**选择 VS Code 的理由**

VS Code 在"轻量"和"强大"之间取得了极佳的平衡：安装包约 200 MB，启动速度远超 PyCharm；通过插件体系，Python 智能提示、调试、格式化等 IDE 级功能一应俱全。而且 VS Code 不只支持 Python——前端、后端、C++、数据科学，一个编辑器就够了。

\end{definitionbox}

### VS Code 安装步骤

#### Windows

1. 访问 [code.visualstudio.com](https://code.visualstudio.com/)，下载 **User Installer**（无需管理员权限）
2. 双击 `.exe`，选择安装路径（建议 `D:\VS Code`，避免含中文或空格）
3. 安装选项建议勾选：
   - "创建桌面快捷方式"
   - "将通过 Code 打开添加到文件上下文菜单"
   - "将通过 Code 打开添加到目录上下文菜单"
4. 点击"安装"，等待完成

#### macOS

1. 下载 `.dmg` 安装包（Intel 和 Apple Silicon 通用）
2. 双击打开后，将 Visual Studio Code 拖入"应用程序"文件夹
3. 首次打开时如遇安全性提示，点击"允许"

#### Ubuntu

```bash
# 下载 .deb 包
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64 -O vscode.deb

# 安装
sudo dpkg -i vscode.deb

# 若提示依赖缺失
sudo apt install -f
```

#### 安装 Python 插件

VS Code 本身是通用编辑器，需要安装 Python 插件才能获得完整的 Python 开发体验：

1. 打开 VS Code，点击左侧"扩展"图标（或按 `Ctrl+Shift+X`）
2. 搜索 **Python**，选择由 Microsoft 发布的版本（下载量最高的那个）
3. 点击"安装"，等待插件启用

#### 配置 Python 解释器

插件安装后，需要告诉 VS Code 使用哪个 Python 运行代码：

1. 按 `Ctrl+Shift+P`，输入 `Python: Select Interpreter`
2. 在列表中选择你的 Python 版本（如 `Python 3.12.4`；Anaconda 用户选择对应环境，如 `base` 或自定义环境名）
3. 配置后，VS Code 右下角状态栏会显示当前关联的 Python 版本

### 用 VS Code 写第一个程序

**创建文件**

`Ctrl+N` 新建文件 → `Ctrl+S` 保存 → 文件名输入 `hello.py` → 保存。`.py` 后缀必须加，这是 VS Code 启用 Python 代码高亮和智能提示的触发器。

**编写代码**

```python
print("Hello, World! 用 VS Code 写 Python 真方便！")
```

**运行程序（四种方式）**

| 方式 | 操作 |
|:-----|:-----|
| 点击运行按钮 | 编辑器右上角 `▶️` 按钮 |
| 右键运行 | 编辑区右键 → "在终端中运行 Python 文件" |
| 快捷键 | `Ctrl+F5`（不调试运行） |
| 终端命令 | 在 VS Code 内置终端中输入 `python hello.py` |

运行后，VS Code 下方终端面板会显示输出结果。

### VS Code 新手核心功能

安装完成后，以下四个功能能让你的编程效率立竿见影：

\begin{tipbox}

**1. 智能代码补全**

输入 `pri`，VS Code 会弹出 `print()` 的自动补全提示，按 `Tab` 键即可补全，减少拼写错误。

**2. 代码格式化**

写多行代码后，按 `Shift+Alt+F`（macOS 为 `Shift+Option+F`），VS Code 会自动调整缩进和空格，让代码格式统一。

**3. 内置终端**

按 `Ctrl+`` `（反引号，键盘左上角）即可在编辑器内打开终端，安装第三方库时无需切换到系统终端。

**4. 错误定位**

代码有语法错误时，问题行会被标红，鼠标悬停即可看到错误说明，帮助新手快速定位问题。

\end{tipbox}

### 常见问题

| 问题 | 解决 |
|:-----|:-----|
| 提示"未选择 Python 解释器" | 按 `Ctrl+Shift+P` → `Python: Select Interpreter` → 选择 Python 版本 |
| 智能提示不生效 | 检查 Python 插件是否已安装并启用；重新选择解释器后重启 VS Code |
| macOS / Linux 提示 `Permission denied` | 终端执行 `chmod +x hello.py` 赋予执行权限 |

### 小结

VS Code 是 Python 学习者的"性价比之王"——没有 IDLE 的功能简陋，也没有 PyCharm 的体积臃肿。掌握基础使用后，随着学习深入，你还可以安装 Jupyter 插件、Git 集成、远程开发等扩展，一器多用，贯穿整个 Python 开发生涯。

---

环境已就绪，编辑器已就位。下一章我们将正式进入 Python 语法核心——从**变量、数据类型和运算符**开始，打下编程的基本功。