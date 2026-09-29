"""个人记账系统 —— 入口"""

import tkinter as tk
from finance_ui import FinanceApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()