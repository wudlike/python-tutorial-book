## 17.3 图形界面开发

天气应用的核心信息已经能在命令行展示了，但用户不会对着黑窗口查天气。本节用 Tkinter 打造一个清爽的桌面天气应用。

### 17.3.1 界面设计草图

```
┌─────────────────────────────────────┐
│  ☀️ 天气查询                        │
├─────────────────────────────────────┤
│  城市: [__________] [🔍 查询]      │
├─────────────────────────────────────┤
│                                     │
│  📍 北京                            │
│  ┌─────────────────────────────┐   │
│  │      ☀️  22°C               │   │
│  │      晴                     │   │
│  │  湿度: 65%   风速: 15km/h   │   │
│  │  体感: 20°C  气压: 1013hPa  │   │
│  └─────────────────────────────┘   │
│                                     │
│  📅 未来天气预报                    │
│  ┌──────┬──────┬──────┐           │
│  │ 周一 │ 周二 │ 周三 │           │
│  │ ☀️   │ ⛅   │ 🌧️   │           │
│  │15~24│16~26│14~20│           │
│  └──────┴──────┴──────┘           │
│                                     │
│  ⏰ 逐小时预报                      │
│  ┌─────────────────────────────┐   │
│  │ 08:00 09:00 10:00 11:00 ... │   │
│  │ 18°C  20°C  21°C  22°C  ...│   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  状态栏: 数据更新时间 2024-06-15   │
│  10:30                               │
└─────────────────────────────────────┘
```

### 17.3.2 主窗口结构

```python
import tkinter as tk
from tkinter import ttk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("天气查询")
        self.root.geometry("480x680")
        self.root.resizable(False, False)

        self.service = WeatherService()
        self._build_search_bar()
        self._build_current_section()
        self._build_forecast_section()
        self._build_hourly_section()
        self._build_status_bar()
```

### 17.3.3 搜索栏

一行搞定：输入框 + 查询按钮，放在顶部最显眼的位置。

```python
def _build_search_bar(self):
    frame = ttk.Frame(self.root, padding=10)
    frame.pack(fill="x")

    ttk.Label(frame, text="城市：").pack(side="left")
    self.city_var = tk.StringVar(value="北京")
    ttk.Entry(frame, textvariable=self.city_var, width=20).pack(side="left", padx=5)
    ttk.Button(frame, text="🔍 查询", command=self._on_search).pack(side="left")

    # 支持回车键触发查询
    self.city_var.trace_add("write", lambda *a: None)
    self.root.bind("<Return>", lambda e: self._on_search())
```

### 17.3.4 当前天气——用 Canvas 手绘卡片

Tkinter 的 `Canvas` 控件可以绘制矩形、文本、颜色块，实现一张漂亮的天气卡片：

```python
def _build_current_section(self):
    """当前天气——Canvas 手绘卡片"""
    self.current_frame = ttk.LabelFrame(self.root, text="当前天气", padding=10)
    self.current_frame.pack(fill="x", padx=10, pady=5)

    self.canvas = tk.Canvas(self.current_frame, height=160, bg="#E3F2FD",
                             highlightthickness=0)
    self.canvas.pack(fill="x")

    # 占位文本
    self.canvas.create_text(200, 80, text="请输入城市并点击查询",
                            font=("Microsoft YaHei", 14), fill="#999")
```

当数据返回后，动态更新 Canvas：

```python
def _show_current(self, city, data):
    self.canvas.delete("all")

    # 根据温度设置背景色
    temp = float(data["temperature"])
    if temp >= 30:    bg = "#FFEBEE"
    elif temp >= 20:  bg = "#E8F5E9"
    elif temp >= 10:  bg = "#E3F2FD"
    else:             bg = "#EDE7F6"
    self.canvas.configure(bg=bg)

    # 城市名 + 天气图标
    display = weather_to_display(data["description"])
    self.canvas.create_text(30, 30, text=f"📍 {city}",
                            font=("Microsoft YaHei", 13, "bold"), anchor="w")

    # 大号温度
    color = temp_color(temp)
    self.canvas.create_text(200, 90, text=f"{temp}°C",
                            font=("Arial", 40, "bold"), fill=color)

    # 天气描述
    self.canvas.create_text(200, 130, text=display,
                            font=("Microsoft YaHei", 12))

    # 详细信息行
    detail_y = 40
    details = [
        f"湿度: {data['humidity']}%",
        f"风速: {data['wind_speed']}km/h",
        f"体感: {data['feels_like']}°C",
    ]
    for i, d in enumerate(details):
        self.canvas.create_text(350, detail_y + i * 22, text=d,
                                font=("Microsoft YaHei", 9), fill="#666")
```

### 17.3.5 未来预报——Frame 矩阵

```python
def _show_forecast(self, forecasts):
    for widget in self.forecast_frame.winfo_children():
        widget.destroy()

    for f in forecasts[:3]:
        card = ttk.Frame(self.forecast_frame, relief="groove", padding=8)
        card.pack(side="left", expand=True, fill="both", padx=3)

        display = weather_to_display(f["description"])
        ttk.Label(card, text=display, font=("Microsoft YaHei", 18)).pack(pady=5)

        ttk.Label(card, text=f['date'][-5:],
                  font=("Microsoft YaHei", 10, "bold")).pack()

        color = temp_color(float(f["max_temp"]))
        ttk.Label(card, text=f"{f['min_temp']}°~{f['max_temp']}°",
                  font=("Microsoft YaHei", 10), foreground=color).pack()
```

### 17.3.6 逐小时预报——水平滚动显示

```python
def _show_hourly(self, hourly_data):
    for widget in self.hourly_frame.winfo_children():
        widget.destroy()

    for h in hourly_data:
        col = ttk.Frame(self.hourly_frame, padding=5)
        col.pack(side="left", padx=4)

        display = weather_to_display(h["description"])
        ttk.Label(col, text=h["time"], font=("Microsoft YaHei", 8)).pack()
        ttk.Label(col, text=display, font=("Microsoft YaHei", 14)).pack()

        color = temp_color(float(h["temperature"]))
        ttk.Label(col, text=f"{h['temperature']}°",
                  font=("Microsoft YaHei", 9, "bold"), foreground=color).pack()
```

> 💡 **完整界面代码**：`projects/weather_app/weather_ui.py`

### 17.3.7 程序入口

```python
# projects/weather_app/main.py
import tkinter as tk
from weather_ui import WeatherApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
```