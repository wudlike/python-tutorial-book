"""个人记账系统 —— 图形界面
Tkinter 界面构建和事件处理
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models import FinanceDB


class FinanceApp:
    CATEGORIES = ["餐饮", "交通", "购物", "住房", "娱乐", "医疗", "教育", "工资", "理财", "其他"]

    def __init__(self, root):
        self.root = root
        self.root.title("个人记账系统")
        self.root.geometry("900x620")
        self.root.minsize(800, 500)

        self.db = FinanceDB()
        self._build_layout()
        self._refresh_list()
        self._refresh_stats()

    # ==================== 布局 ====================

    def _build_layout(self):
        left_frame = ttk.Frame(self.root, padding=5)
        left_frame.pack(side="left", fill="y")

        right_frame = ttk.Frame(self.root, padding=5)
        right_frame.pack(side="left", fill="both", expand=True)

        self._build_input_area(left_frame)
        self._build_filter_area(left_frame)
        self._build_record_list(right_frame)
        self._build_stats_area(right_frame)

    def _build_input_area(self, parent):
        frame = ttk.LabelFrame(parent, text="添加记录", padding=10)
        frame.pack(fill="x", pady=(0, 5))

        ttk.Label(frame, text="类型：").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="expense")
        ttk.Radiobutton(frame, text="支出", variable=self.type_var, value="expense").grid(row=0, column=1)
        ttk.Radiobutton(frame, text="收入", variable=self.type_var, value="income").grid(row=0, column=2)

        ttk.Label(frame, text="类别：").grid(row=1, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.category_var, values=self.CATEGORIES, width=13).grid(
            row=1, column=1, columnspan=2, sticky="ew")

        ttk.Label(frame, text="金额：").grid(row=2, column=0, sticky="w", pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.amount_var, width=15).grid(row=2, column=1, columnspan=2, sticky="ew")

        ttk.Label(frame, text="日期：").grid(row=3, column=0, sticky="w", pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(frame, textvariable=self.date_var, width=15).grid(row=3, column=1, columnspan=2, sticky="ew")

        ttk.Label(frame, text="备注：").grid(row=4, column=0, sticky="w", pady=5)
        self.note_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.note_var, width=15).grid(row=4, column=1, columnspan=2, sticky="ew")

        ttk.Button(frame, text="添加记录", command=self._on_add).grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(frame, text="清空输入", command=self._clear_input).grid(row=6, column=0, columnspan=3)

    def _build_filter_area(self, parent):
        frame = ttk.LabelFrame(parent, text="筛选", padding=10)
        frame.pack(fill="x", pady=5)

        ttk.Label(frame, text="类型：").grid(row=0, column=0, sticky="w")
        self.filter_type = tk.StringVar(value="全部")
        ttk.Combobox(frame, textvariable=self.filter_type, values=["全部", "income", "expense"],
                     width=10, state="readonly").grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="类别：").grid(row=1, column=0, sticky="w", pady=5)
        self.filter_category = tk.StringVar(value="全部")
        ttk.Combobox(frame, textvariable=self.filter_category,
                     values=["全部"] + self.CATEGORIES, width=10, state="readonly").grid(
            row=1, column=1, sticky="ew")

        ttk.Button(frame, text="刷新列表", command=self._refresh_list).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="导出 CSV", command=self._on_export).grid(row=3, column=0, columnspan=2)

    def _build_record_list(self, parent):
        list_frame = ttk.LabelFrame(parent, text="账单记录", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 5))

        columns = ("id", "date", "type", "category", "amount", "note")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="日期")
        self.tree.heading("type", text="类型")
        self.tree.heading("category", text="类别")
        self.tree.heading("amount", text="金额")
        self.tree.heading("note", text="备注")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=100)
        self.tree.column("type", width=60)
        self.tree.column("category", width=80)
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("note", width=200)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(side="bottom", fill="x", pady=(5, 0))
        ttk.Button(btn_frame, text="编辑选中", command=self._on_edit).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="删除选中", command=self._on_delete).pack(side="left", padx=2)

    def _build_stats_area(self, parent):
        self.stats_frame = ttk.LabelFrame(parent, text="统计概览", padding=10)
        self.stats_frame.pack(fill="x")

        self.stats_text = tk.Text(self.stats_frame, height=6, width=60, state="disabled",
                                   font=("Consolas", 10))
        self.stats_text.pack(fill="both")

    # ==================== 事件处理 ====================

    def _on_add(self):
        trans_type = self.type_var.get()
        category = self.category_var.get().strip()
        amount_str = self.amount_var.get().strip()
        date = self.date_var.get().strip()
        note = self.note_var.get().strip()

        if not category:
            messagebox.showwarning("提示", "请选择类别")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("错误", "金额必须是数字")
            return
        if amount <= 0:
            messagebox.showerror("错误", "金额必须大于 0")
            return
        if not date:
            messagebox.showwarning("提示", "请输入日期")
            return

        trans_id = self.db.add_transaction(trans_type, category, amount, date, note)
        messagebox.showinfo("成功", f"记录已添加 (ID: {trans_id})")
        self._clear_input()
        self._refresh_list()
        self._refresh_stats()

    def _clear_input(self):
        self.category_var.set("")
        self.amount_var.set("")
        self.note_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def _on_edit(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一条记录")
            return

        item = self.tree.item(selection[0])
        values = item["values"]
        trans_id = values[0]
        current = {"date": values[1], "type": values[2],
                   "category": values[3], "amount": values[4], "note": values[5]}

        dialog = EditDialog(self.root, current)
        self.root.wait_window(dialog)

        if dialog.result:
            self.db.update_transaction(trans_id, **dialog.result)
            self._refresh_list()
            self._refresh_stats()
            messagebox.showinfo("成功", "记录已更新")

    def _on_delete(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一条记录")
            return

        if not messagebox.askyesno("确认", "确定要删除选中的记录吗？"):
            return

        for item in selection:
            trans_id = self.tree.item(item)["values"][0]
            self.db.delete_transaction(trans_id)

        self._refresh_list()
        self._refresh_stats()
        messagebox.showinfo("成功", "记录已删除")

    def _on_export(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV 文件", "*.csv")],
            initialfile=f"记账数据_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        if filepath:
            count = self.db.export_csv(filepath)
            messagebox.showinfo("成功", f"已导出 {count} 条记录到\n{filepath}")

    # ==================== 数据刷新 ====================

    def _refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        trans_type = None if self.filter_type.get() == "全部" else self.filter_type.get()
        category = None if self.filter_category.get() == "全部" else self.filter_category.get()

        records = self.db.get_transactions(trans_type=trans_type, category=category)
        for r in records:
            amount_display = f"{'+' if r['type']=='income' else '-'}¥{r['amount']:.2f}"
            self.tree.insert("", "end", values=(
                r["id"], r["date"],
                "收入" if r["type"] == "income" else "支出",
                r["category"], amount_display, r["note"]
            ))

    def _refresh_stats(self):
        now = datetime.now()
        stats = self.db.get_statistics(year=now.year, month=now.month)

        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", "end")

        lines = [
            f"📊 {now.year}年{now.month}月 统计",
            f"{'─' * 30}",
            f"💰 总收入：¥{stats['total_income']:,.2f}",
            f"💸 总支出：¥{stats['total_expense']:,.2f}",
            f"📈 结  余：¥{stats['total_income'] - stats['total_expense']:,.2f}",
            f"{'─' * 30}",
        ]
        for cat, total in stats["by_category"]:
            lines.append(f"  {cat}: ¥{total:,.2f}")

        self.stats_text.insert("1.0", "\n".join(lines))
        self.stats_text.configure(state="disabled")


class EditDialog(tk.Toplevel):
    def __init__(self, parent, current):
        super().__init__(parent)
        self.title("编辑记录")
        self.geometry("300x250")
        self.resizable(False, False)
        self.result = None

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="日期：").grid(row=0, column=0, sticky="w", pady=3)
        self.date_var = tk.StringVar(value=current["date"])
        ttk.Entry(frame, textvariable=self.date_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="类别：").grid(row=1, column=0, sticky="w", pady=3)
        self.category_var = tk.StringVar(value=current["category"])
        ttk.Combobox(frame, textvariable=self.category_var,
                     values=FinanceApp.CATEGORIES).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="金额：").grid(row=2, column=0, sticky="w", pady=3)
        self.amount_var = tk.StringVar(value=current["amount"].replace("¥", "").lstrip("+-"))
        ttk.Entry(frame, textvariable=self.amount_var).grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="备注：").grid(row=3, column=0, sticky="w", pady=3)
        self.note_var = tk.StringVar(value=current["note"])
        ttk.Entry(frame, textvariable=self.note_var).grid(row=3, column=1, sticky="ew")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="保存", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side="left", padx=5)

        self.transient(parent)
        self.grab_set()

    def _on_save(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("错误", "金额必须是数字", parent=self)
            return

        self.result = {
            "date": self.date_var.get(),
            "category": self.category_var.get(),
            "amount": amount,
            "note": self.note_var.get(),
        }
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()