"""个人记账系统 —— 数据库层
SQLite 数据库的创建、CRUD 操作、统计分析
"""

import sqlite3
from datetime import datetime


class FinanceDB:
    def __init__(self, db_path="finance.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                type       TEXT    NOT NULL,
                category   TEXT    NOT NULL,
                amount     REAL    NOT NULL,
                date       TEXT    NOT NULL,
                note       TEXT    DEFAULT '',
                created_at TEXT    DEFAULT (datetime('now','localtime'))
            )
        """)
        self.conn.commit()

    def add_transaction(self, trans_type, category, amount, date, note=""):
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO transactions (type, category, amount, date, note) VALUES (?, ?, ?, ?, ?)",
                (trans_type, category, amount, date, note)
            )
        return cursor.lastrowid

    def get_transactions(self, trans_type=None, category=None, start_date=None, end_date=None):
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if trans_type:
            query += " AND type = ?"
            params.append(trans_type)
        if category:
            query += " AND category = ?"
            params.append(category)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date DESC, id DESC"
        return [dict(row) for row in self.conn.execute(query, params).fetchall()]

    def update_transaction(self, trans_id, **kwargs):
        allowed = {"type", "category", "amount", "date", "note"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [trans_id]

        with self.conn:
            self.conn.execute(
                f"UPDATE transactions SET {set_clause} WHERE id = ?", values
            )
        return True

    def delete_transaction(self, trans_id):
        with self.conn:
            self.conn.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        return True

    def get_statistics(self, year=None, month=None):
        conditions = "WHERE 1=1"
        params = []

        if year:
            conditions += " AND strftime('%Y', date) = ?"
            params.append(str(year))
        if month:
            conditions += " AND strftime('%m', date) = ?"
            params.append(f"{int(month):02d}")

        by_category = self.conn.execute(
            f"SELECT category, SUM(amount) as total FROM transactions {conditions} "
            f"GROUP BY category ORDER BY total DESC", params
        ).fetchall()

        by_month = self.conn.execute(
            f"SELECT strftime('%m', date) as month, type, SUM(amount) as total "
            f"FROM transactions {conditions} GROUP BY month, type ORDER BY month",
            params
        ).fetchall()

        total_income = self.conn.execute(
            f"SELECT COALESCE(SUM(amount), 0) FROM transactions {conditions} AND type='income'",
            params
        ).fetchone()[0]

        total_expense = self.conn.execute(
            f"SELECT COALESCE(SUM(amount), 0) FROM transactions {conditions} AND type='expense'",
            params
        ).fetchone()[0]

        return {
            "by_category": [(r[0], r[1]) for r in by_category],
            "by_month": [(r[0], r[1], r[2]) for r in by_month],
            "total_income": total_income,
            "total_expense": total_expense,
        }

    def export_csv(self, filepath):
        import csv
        rows = self.conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "类型", "类别", "金额", "日期", "备注", "创建时间"])
            for r in rows:
                writer.writerow([r["id"], r["type"], r["category"],
                                r["amount"], r["date"], r["note"], r["created_at"]])
        return len(rows)

    def close(self):
        self.conn.close()