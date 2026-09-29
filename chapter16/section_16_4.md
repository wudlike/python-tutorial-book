## 16.4 界面开发（Tkinter）

Tkinter 是 Python 自带的图形界面库，无需额外安装。虽然它的外观不如现代 Web 界面精致，但对于工具型应用来说完全够用——启动快、打包小、零依赖。

### 16.4.1 界面总览

记账系统的界面分为三大区域：

```
┌─────────────────────────────────────┐
│  💰 个人记账系统                    │  ← 标题栏
├──────────────┬──────────────────────┤
│  输入区域     │                      │
│  类型: [收入] │   记录列表            │
│  类别: [餐饮] │  ┌──────────────────┐│
│  金额: [____] │  │ 日期  类别 金额  ││
│  日期: [____] │  │ 06-01 餐饮 -35  ││
│  备注: [____] │  │ 06-01 工资+8000││
│  [添加记录]   │  └──────────────────┘│
│              │  [编辑] [删除] [导出] │
│  筛选区域     │                      │
│  类型: [全部] │   月度统计            │
│  月份: [06月] │  ┌──────────────────┐│
│  [刷新列表]   │  │ 收入: ¥8500     ││
│              │  │ 支出: ¥3200     ││
│              │  │ 结余: ¥5300     ││
│              │  └──────────────────┘│
└──────────────┴──────────────────────┘
```

### 16.4.2 主窗口骨架

```python
import tkinter as tk
from tkinter import ttk, messagebox

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人记账系统")
        self.root.geometry("900x600")

        # 连接数据库
        self.db = FinanceDB()

        # 构建界面
        self._build_input_area()
        self._build_record_list()
        self._build_stats_area()
```

Tkinter 中，`Frame` 是容器控件。把不同功能区放在不同的 Frame 中，每个 Frame 用独立的 `_build_xxx` 方法构建，结构清晰，便于维护。

### 16.4.3 输入区域实现

```python
def _build_input_area(self):
    frame = ttk.LabelFrame(self.root, text="添加记录", padding=10)
    frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # 类型选择
    ttk.Label(frame, text="类型：").grid(row=0, column=0, sticky="w")
    self.type_var = tk.StringVar(value="expense")
    ttk.Radiobutton(frame, text="支出", variable=self.type_var,
                    value="expense").grid(row=0, column=1)
    ttk.Radiobutton(frame, text="收入", variable=self.type_var,
                    value="income").grid(row=0, column=2)

    # 类别下拉框
    ttk.Label(frame, text="类别：").grid(row=1, column=0, sticky="w", pady=5)
    self.category_var = tk.StringVar()
    categories = ["餐饮", "交通", "购物", "住房", "娱乐", "医疗", "教育", "工资", "理财", "其他"]
    ttk.Combobox(frame, textvariable=self.category_var,
                 values=categories).grid(row=1, column=1, columnspan=2, sticky="ew")

    # 金额输入
    ttk.Label(frame, text="金额：").grid(row=2, column=0, sticky="w", pady=5)
    self.amount_var = tk.StringVar()
    ttk.Entry(frame, textvariable=self.amount_var).grid(row=2, column=1, columnspan=2, sticky="ew")

    # 日期输入
    ttk.Label(frame, text="日期：").grid(row=3, column=0, sticky="w", pady=5)
    self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    ttk.Entry(frame, textvariable=self.date_var).grid(row=3, column=1, columnspan=2, sticky="ew")

    # 备注
    ttk.Label(frame, text="备注：").grid(row=4, column=0, sticky="w", pady=5)
    self.note_var = tk.StringVar()
    ttk.Entry(frame, textvariable=self.note_var).grid(row=4, column=1, columnspan=2, sticky="ew")

    # 按钮
    ttk.Button(frame, text="添加记录", command=self._on_add).grid(
        row=5, column=0, columnspan=3, pady=10)
```

### 16.4.4 记录列表——Treeview

Tkinter 的 `ttk.Treeview` 是显示表格数据的最佳控件：

```python
def _build_record_list(self):
    frame = ttk.LabelFrame(self.root, text="账单记录", padding=10)
    frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

    columns = ("id", "date", "type", "category", "amount", "note")
    self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    self.tree.heading("id", text="ID")
    self.tree.heading("date", text="日期")
    self.tree.heading("type", text="类型")
    self.tree.heading("category", text="类别")
    self.tree.heading("amount", text="金额")
    self.tree.heading("note", text="备注")

    self.tree.column("id", width=40)
    self.tree.column("date", width=100)
    self.tree.column("type", width=60)
    self.tree.column("category", width=80)
    self.tree.column("amount", width=80)
    self.tree.column("note", width=150)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
    self.tree.configure(yscrollcommand=scrollbar.set)
    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
```

`Treeview` 的列设置包含列名、标题和宽度，一行一个列配置。加上滚动条后，即使数据上千条也能流畅浏览。

### 16.4.5 事件处理——按钮回调

每个按钮点击时触发对应的回调方法：

```python
def _on_add(self):
    """处理添加记录按钮"""
    try:
        amount = float(self.amount_var.get())
    except ValueError:
        messagebox.showerror("错误", "金额必须是数字")
        return

    success, msg = add_record(
        self.db,
        self.type_var.get(),
        self.category_var.get(),
        amount,
        self.date_var.get(),
        self.note_var.get()
    )
    if success:
        messagebox.showinfo("成功", msg)
        self._refresh_list()
        self._refresh_stats()
    else:
        messagebox.showerror("错误", msg)
```

`messagebox` 提供标准的对话框——`showinfo`（信息）、`showerror`（错误）、`askyesno`（确认），比 `print()` 更适合图形界面应用。

> 💡 **完整界面代码**：`projects/personal_finance/finance_ui.py`，约 200 行，包含完整的窗口布局和事件处理逻辑。

### 16.4.6 程序入口——`main.py`

```python
# projects/personal_finance/main.py
import tkinter as tk
from finance_ui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
```

运行 `python main.py` 即可启动完整的记账系统。