## 16.5 打包发布

写好的程序如果只能在安装了 Python 的电脑上运行，分享给别人就太麻烦了。本节使用 PyInstaller 把 Python 程序打包成独立的 `.exe` 可执行文件——对方不需要安装任何 Python 环境，双击就能运行。

### 16.5.1 安装 PyInstaller

```bash
pip install pyinstaller
```

### 16.5.2 基本打包命令

在项目目录下执行：

```bash
cd projects/personal_finance
pyinstaller --onefile --windowed main.py
```

参数说明：
- `--onefile`：所有依赖打包成一个单独的 `.exe` 文件，分发方便
- `--windowed`（或 `-w`）：不显示命令行黑窗口（GUI 程序专用）
- `--name`：指定输出文件名，默认与入口文件同名
- `--icon=app.ico`：设置程序图标

打包完成后，在 `dist/` 目录下找到 `main.exe`，把这个文件发给任何人就可以直接运行了。

### 16.5.3 加入图标和版本信息

```bash
pyinstaller --onefile --windowed --name="个人记账" --icon=icon.ico main.py
```

还可以创建 `.spec` 文件做更精细的控制（如排除不需要的库来减小体积）：

```bash
# 先生成 spec 文件
pyinstaller --onefile --windowed --name="个人记账" main.py

# 之后直接编辑 main.spec，再执行
pyinstaller main.spec
```

### 16.5.4 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 打包后找不到数据库 | 工作目录变了 | 使用 `os.path.dirname(sys.argv[0])` 获取 exe 所在目录 |
| 被杀毒软件拦截 | PyInstaller 打包的特征被误报 | 使用 `--windowed`、提交误报申诉 |
| 文件太大（>30MB） | 打包了不必要的库 | 在 spec 文件中 `excludes` 排除未使用的模块 |
| 中文路径报错 | 编码问题 | 确保所有路径使用英文 |

### 16.5.5 完整发布清单

一个完整的"发布包"应包括：

```
个人记账系统_v1.0/
├── 个人记账.exe         ← 主程序
├── README.txt           ← 使用说明
└── icon.ico             ← 程序图标
```

> 💡 跨平台注意：PyInstaller 在哪个平台打包，生成的可执行文件就只能在哪个平台运行。Windows 上打包生成 `.exe`；macOS 上生成 `.app`；Linux 上生成无后缀的可执行文件。要支持多平台，需要在对应的操作系统上分别打包。

### 实战练习

1. 为记账系统增加"预算预警"功能——用户可以为每个类别设置月预算，当月支出接近或超过预算时显示红色警告。

2. 增加数据备份与恢复功能——点击"备份"将数据库文件复制到指定位置，点击"恢复"从备份文件还原数据。

3. 将记账系统用 PyInstaller 打包成 `.exe`，在自己的电脑上测试运行是否正常，然后发给朋友试用并收集反馈。