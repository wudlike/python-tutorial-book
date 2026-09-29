## 16.5 实战练习

### 练习1：预算预警

**答案：**

在 `models.py` 中添加预算表：

```python
# 在 _create_tables 中添加
self.conn.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        category TEXT PRIMARY KEY,
        monthly_budget REAL NOT NULL
    )
""")

def set_budget(self, category, monthly_budget):
    with self.conn:
        self.conn.execute(
            "INSERT OR REPLACE INTO budgets (category, monthly_budget) VALUES (?, ?)",
            (category, monthly_budget)
        )

def get_budgets(self):
    rows = self.conn.execute("SELECT * FROM budgets").fetchall()
    return {r["category"]: r["monthly_budget"] for r in rows}

def check_budget_alerts(self, year, month):
    budgets = self.get_budgets()
    alerts = []
    stats = self.get_statistics(year=year, month=month)
    for cat, spent in stats["by_category"]:
        if cat in budgets:
            pct = spent / budgets[cat] * 100
            if pct >= 100:
                alerts.append(f"⚠️ {cat}: 已超预算！¥{spent:.0f}/¥{budgets[cat]:.0f}")
            elif pct >= 80:
                alerts.append(f"⚡ {cat}: 即将超预算 ¥{spent:.0f}/¥{budgets[cat]:.0f}")
    return alerts
```

在 `finance_ui.py` 中添加预算设置界面和警告显示：

```python
def _build_budget_area(self, parent):
    frame = ttk.LabelFrame(parent, text="预算管理", padding=10)
    frame.pack(fill="x", pady=5)
    # 类别选择 + 金额输入 + 设置按钮
    ...

def _refresh_stats(self):
    # ...原有代码...
    alerts = self.db.check_budget_alerts(now.year, now.month)
    if alerts:
        lines.append(f"{'─' * 30}")
        lines.append("🚨 预算警告：")
        lines.extend(alerts)
```

---

### 练习2：数据备份与恢复

**答案：**

```python
import shutil
from datetime import datetime

class FinanceDB:
    # ...原有代码...

    def backup(self, backup_dir="backups"):
        import os
        os.makedirs(backup_dir, exist_ok=True)
        self.conn.close()  # 先关闭连接确保数据刷新到磁盘

        filename = f"finance_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(backup_dir, filename)
        shutil.copy2(self.db_path, backup_path)

        # 重新连接
        self.__init__(self.db_path)
        return backup_path

    def restore(self, backup_path):
        self.conn.close()
        shutil.copy2(backup_path, self.db_path)
        self.__init__(self.db_path)
```

在界面中添加备份/恢复按钮：

```python
def _on_backup(self):
    path = self.db.backup()
    messagebox.showinfo("成功", f"数据已备份到:\n{path}")

def _on_restore(self):
    filepath = filedialog.askopenfilename(
        filetypes=[("数据库文件", "*.db")],
        title="选择备份文件"
    )
    if filepath and messagebox.askyesno("确认", "恢复将覆盖当前数据，确定吗？"):
        self.db.restore(filepath)
        self._refresh_list()
        self._refresh_stats()
        messagebox.showinfo("成功", "数据已恢复")
```

---

### 练习3：PyInstaller 打包

**答案：**

```bash
cd projects/personal_finance

# 生成 spec 文件
pyinstaller --onefile --windowed --name="个人记账" main.py

# 如果打包后提示缺少 tkinter 或 sqlite3，使用 hidden-import
pyinstaller --onefile --windowed --name="个人记账" \
    --hidden-import=tkinter \
    --hidden-import=sqlite3 \
    main.py

# 打包含图标
pyinstaller --onefile --windowed --name="个人记账" \
    --icon=app.ico main.py

# 输出在 dist/个人记账.exe
```

在代码中处理数据库路径：

```python
import sys
import os

def get_db_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "finance.db")
```


## 17.4 实战练习

### 练习1：收藏城市

**答案：**

```python
import json
import os

class CityFavorites:
    def __init__(self, filepath="favorites.json"):
        self.filepath = filepath
        self.cities = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.cities, f, ensure_ascii=False, indent=2)

    def add(self, city):
        if city not in self.cities:
            self.cities.append(city)
            self._save()
            return True
        return False

    def remove(self, city):
        if city in self.cities:
            self.cities.remove(city)
            self._save()
            return True
        return False

    def get_all(self):
        return self.cities
```

在 UI 中添加收藏功能：

```python
def _build_favorites(self, parent):
    frame = ttk.LabelFrame(parent, text="收藏城市", padding=5)
    frame.pack(fill="x", pady=5)

    self.favorites_listbox = tk.Listbox(frame, height=4)
    self.favorites_listbox.pack(side="left", fill="both", expand=True)
    self.favorites_listbox.bind("<Double-Button-1>", self._on_favorite_click)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(side="right", fill="y")
    ttk.Button(btn_frame, text="★", command=self._on_add_favorite).pack(pady=2)
    ttk.Button(btn_frame, text="✕", command=self._on_remove_favorite).pack(pady=2)

    self._refresh_favorites()

def _on_add_favorite(self):
    city = self.city_var.get().strip()
    if city:
        self.favorites.add(city)
        self._refresh_favorites()

def _on_remove_favorite(self):
    sel = self.favorites_listbox.curselection()
    if sel:
        city = self.favorites_listbox.get(sel[0])
        self.favorites.remove(city)
        self._refresh_favorites()

def _on_favorite_click(self, event):
    sel = self.favorites_listbox.curselection()
    if sel:
        city = self.favorites_listbox.get(sel[0])
        self.city_var.set(city)
        self._on_search()

def _refresh_favorites(self):
    self.favorites_listbox.delete(0, "end")
    for city in self.favorites.get_all():
        self.favorites_listbox.insert("end", city)
```

---

### 练习2：天气预警

**答案：**

```python
import schedule
import time
from datetime import datetime

WARNING_KEYWORDS = {
    "暴雨": ["Heavy rain", "rain", "thunder"],
    "高温": ["35", "36", "37", "38", "39", "40"],
    "大风": ["gale", "strong wind"],
}

def check_weather_warnings(city, favorites):
    """检查收藏城市的天气预警"""
    try:
        data = WeatherService.get_current(city)
        forecast = WeatherService.get_forecast(city, days=1)

        warnings = []

        # 检查当前天气
        desc = data["description"].lower()
        for alert, keywords in WARNING_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in desc:
                    warnings.append(f"{city}: {alert}预警（当前{data['description']}）")
                    break

        # 检查高温
        max_temp = float(forecast[0]["max_temp"])
        if max_temp >= 35:
            warnings.append(f"{city}: 高温预警（最高{max_temp}°C）")

        return warnings
    except Exception as e:
        return [f"{city}: 查询失败 ({e})"]

def scheduled_warning_check(favorites):
    warnings = []
    for city in favorites.get_all():
        warnings.extend(check_weather_warnings(city, favorites))

    if warnings:
        # 发送系统通知（Windows）
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("天气预警", "\n".join(warnings[:3]), duration=10)
        except ImportError:
            print("\n".join(warnings))

schedule.every().day.at("07:00").do(scheduled_warning_check, favorites)

print("天气预警系统已启动...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

### 练习3：API 降级

**答案：**

```python
import requests

class RobustWeatherService:
    """支持多 API 降级的天气服务"""

    API_LIST = [
        {
            "name": "wttr.in",
            "url_template": "https://wttr.in/{city}?format=j1",
            "parser": "_parse_wttrin",
        },
        # 备用 API（需要注册 Key）
        # {
        #     "name": "OpenWeatherMap",
        #     "url_template": "https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_KEY&units=metric",
        #     "parser": "_parse_openweather",
        # },
    ]

    def get_current(self, city):
        errors = []
        for api in self.API_LIST:
            try:
                url = api["url_template"].format(city=city)
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                parser = getattr(self, api["parser"])
                return parser(response.json()), api["name"]
            except Exception as e:
                errors.append(f"  {api['name']}: {e}")
                continue

        raise Exception(f"所有 API 均不可用:\n" + "\n".join(errors))

    def _parse_wttrin(self, data):
        current = data["current_condition"][0]
        return {
            "temperature": current["temp_C"],
            "humidity": current["humidity"],
            "description": current["weatherDesc"][0]["value"],
            "source": "wttr.in",
        }

    def _parse_openweather(self, data):
        return {
            "temperature": str(data["main"]["temp"]),
            "humidity": str(data["main"]["humidity"]),
            "description": data["weather"][0]["description"],
            "source": "OpenWeatherMap",
        }
```