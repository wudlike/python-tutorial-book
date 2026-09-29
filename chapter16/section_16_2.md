## 16.2 数据库设计（SQLite）

数据库是记账系统的"记忆中枢"。所有账单数据都存储在这里，程序重启后数据也不会丢失。本节使用 SQLite——它轻量、零配置、Python 内置支持，非常适合单机应用。

### 16.2.1 数据表设计

只需要一张表来存储所有账单记录：

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,   -- 唯一编号
    type        TEXT    NOT NULL,                     -- 类型: income / expense
    category    TEXT    NOT NULL,                     -- 类别: 餐饮、交通、工资...
    amount      REAL    NOT NULL,                     -- 金额
    date        TEXT    NOT NULL,                     -- 日期: YYYY-MM-DD
    note        TEXT    DEFAULT '',                   -- 备注
    created_at  TEXT    DEFAULT (datetime('now','localtime'))  -- 记录创建时间
);
```

字段说明：
- `id`：自增主键，每笔记录的唯一标识
- `type`：收入（`income`）或支出（`expense`）
- `category`：分类维度，如"餐饮"、"交通"、"工资"、"购物"等
- `amount`：金额，使用 REAL 类型支持小数
- `date`：发生日期，格式 `YYYY-MM-DD`
- `note`：可选的备注信息
- `created_at`：记录创建时间，用于追踪数据录入时间

### 16.2.2 数据层的封装——`models.py`

把数据库操作封装成一个类，上层代码不需要直接写 SQL。核心文件见：`projects/personal_finance/models.py`

它的对外接口如下：

```python
class FinanceDB:
    def __init__(self, db_path="finance.db"):
        """连接数据库，自动建表"""
        ...

    def add_transaction(self, trans_type, category, amount, date, note=""):
        """添加一笔记录 → 返回记录 id"""
        ...

    def get_transactions(self, trans_type=None, category=None,
                         start_date=None, end_date=None):
        """查询记录列表，支持按类型/类别/日期筛选 → 返回列表"""
        ...

    def update_transaction(self, trans_id, **kwargs):
        """更新一条记录"""
        ...

    def delete_transaction(self, trans_id):
        """删除一条记录"""
        ...

    def get_statistics(self, year=None, month=None):
        """统计分析——按类别汇总、按月份汇总 → 返回字典"""
        ...

    def export_csv(self, filepath):
        """导出全部数据到 CSV 文件"""
        ...
```

> 💡 **完整代码**请查看 `projects/personal_finance/models.py`。由于代码较长（约 120 行），书中不再逐行列出，以免占用过多篇幅。

### 16.2.3 关键实现要点

**参数化查询防注入**：

```python
# ✅ 正确：使用参数占位符
self.conn.execute(
    "SELECT * FROM transactions WHERE type = ?", (trans_type,)
)

# ❌ 错误：字符串拼接（SQL注入风险）
self.conn.execute(f"SELECT * FROM transactions WHERE type = '{trans_type}'")
```

**统计查询的核心 SQL**：

```python
# 按类别统计——使用 GROUP BY 聚合
SELECT category, SUM(amount) as total
FROM transactions
WHERE type = 'expense' AND date BETWEEN ? AND ?
GROUP BY category
ORDER BY total DESC
```

**上下文管理器管理连接**：

使用 `with self.conn:` 确保事务自动提交或回滚，即使中途出错也不会留下不完整的数据。