## 16.3 功能实现

本节实现记账系统的核心业务逻辑——对接数据库层和界面层之间的"翻译官"角色。所有增删改查操作通过这些函数完成，确保界面代码和数据库代码完全解耦。

### 16.3.1 添加记录

用户输入金额、选择类别和日期后，调用此函数将记录写入数据库：

```python
def add_record(db, trans_type, category, amount, date, note=""):
    """添加一笔记录并返回成功信息"""
    if amount <= 0:
        return False, "金额必须大于 0"

    trans_id = db.add_transaction(trans_type, category, amount, date, note)
    return True, f"记录已添加 (ID: {trans_id})"
```

关键点：在写入数据库**之前**做数据校验（金额必须为正数），避免脏数据入库。

### 16.3.2 筛选与查询

支持多种筛选条件的组合查询：

```python
def query_records(db, trans_type="全部", category="全部",
                  start_date=None, end_date=None):
    """按条件查询记录列表"""
    t = None if trans_type == "全部" else trans_type
    c = None if category == "全部" else category
    records = db.get_transactions(
        trans_type=t, category=c,
        start_date=start_date, end_date=end_date
    )
    return records
```

用户界面中的下拉框选项包含"全部"，对应到这里就是把参数转为 `None`（不筛选）。

### 16.3.3 统计分析

统计模块计算两个维度的数据：

**（1）按类别汇总**——回答"钱都花在哪些地方了？"

```python
def get_category_stats(db, year, month):
    """返回 {类别: 金额} 的字典"""
    stats = db.get_statistics(year=year, month=month)
    by_category = {}
    for row in stats["by_category"]:
        by_category[row[0]] = row[1]
    return by_category
```

**（2）按月份汇总**——回答"这个月的收支情况如何？"

```python
def get_monthly_summary(db, year):
    """返回 [(月份, 收入, 支出), ...]"""
    stats = db.get_statistics(year=year)
    # 按月份组织数据
    monthly = {}
    for row in stats["by_month"]:
        month, trans_type, total = row[0], row[1], row[2]
        if month not in monthly:
            monthly[month] = {"income": 0, "expense": 0}
        monthly[month][trans_type] = total
    return [(m, v["income"], v["expense"]) for m, v in sorted(monthly.items())]
```

### 16.3.4 导出 CSV

将数据库内容导出为 Excel 可打开的 CSV 文件：

```python
def export_to_csv(db, filepath):
    """导出全部记录为 CSV"""
    try:
        count = db.export_csv(filepath)
        return True, f"成功导出 {count} 条记录到 {filepath}"
    except Exception as e:
        return False, f"导出失败：{e}"
```

> 💡 **完整代码**：`projects/personal_finance/finance_logic.py`，包含了所有业务逻辑函数的完整实现。