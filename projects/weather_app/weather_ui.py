"""天气查询应用 —— 图形界面
Tkinter 天气查询桌面应用
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

from weather_service import WeatherService
from weather_display import weather_to_display, temp_color


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("天气查询")
        self.root.geometry("480x680")
        self.root.resizable(False, False)

        self.service = WeatherService()
        self._cache = {}       # {city: (data, timestamp)}
        self._loading = False

        self._build_search_bar()
        self._build_current_section()
        self._build_forecast_section()
        self._build_hourly_section()
        self._build_status_bar()

    # ==================== 搜索栏 ====================

    def _build_search_bar(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="城市：").pack(side="left")
        self.city_var = tk.StringVar(value="北京")
        city_entry = ttk.Entry(frame, textvariable=self.city_var, width=20)
        city_entry.pack(side="left", padx=5)
        city_entry.bind("<Return>", lambda e: self._on_search())

        self.search_btn = ttk.Button(frame, text="🔍 查询", command=self._on_search)
        self.search_btn.pack(side="left")

    # ==================== 当前天气 ====================

    def _build_current_section(self):
        self.current_frame = ttk.LabelFrame(self.root, text="当前天气", padding=10)
        self.current_frame.pack(fill="x", padx=10, pady=5)

        self.canvas = tk.Canvas(self.current_frame, height=160, bg="#E3F2FD",
                                 highlightthickness=0)
        self.canvas.pack(fill="x")
        self.canvas.create_text(200, 80, text="请输入城市并点击查询",
                                font=("Microsoft YaHei", 14), fill="#999")

    def _show_current(self, city, data):
        self.canvas.delete("all")

        temp = float(data["temperature"])
        if temp >= 30:
            bg = "#FFEBEE"
        elif temp >= 20:
            bg = "#E8F5E9"
        elif temp >= 10:
            bg = "#E3F2FD"
        else:
            bg = "#EDE7F6"
        self.canvas.configure(bg=bg)

        display = weather_to_display(data["description"])
        self.canvas.create_text(30, 30, text=f"📍 {city}",
                                font=("Microsoft YaHei", 13, "bold"), anchor="w")

        color = temp_color(temp)
        self.canvas.create_text(180, 85, text=f"{temp}°C",
                                font=("Arial", 40, "bold"), fill=color)

        self.canvas.create_text(200, 130, text=display,
                                font=("Microsoft YaHei", 12))

        details = [
            f"湿度: {data['humidity']}%",
            f"风速: {data['wind_speed']}km/h",
            f"体感: {data['feels_like']}°C",
        ]
        for i, d in enumerate(details):
            self.canvas.create_text(350, 30 + i * 22, text=d,
                                    font=("Microsoft YaHei", 9), fill="#555")

    # ==================== 未来预报 ====================

    def _build_forecast_section(self):
        self.forecast_frame = ttk.LabelFrame(self.root, text="未来预报", padding=10)
        self.forecast_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(self.forecast_frame, text="输入城市查询天气预报").pack()

    def _show_forecast(self, forecasts):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.forecast_frame)
        container.pack()

        for f in forecasts[:3]:
            card = ttk.Frame(container, relief="groove", padding=10)
            card.pack(side="left", padx=5)

            display = weather_to_display(f["description"])
            ttk.Label(card, text=display, font=("Microsoft YaHei", 22)).pack(pady=5)
            ttk.Label(card, text=f['date'][-5:], font=("Microsoft YaHei", 10, "bold")).pack()

            color = temp_color(float(f["max_temp"]))
            ttk.Label(card, text=f"{f['min_temp']}°~{f['max_temp']}°",
                      font=("Microsoft YaHei", 10)).pack()

    # ==================== 逐小时预报 ====================

    def _build_hourly_section(self):
        self.hourly_frame = ttk.LabelFrame(self.root, text="逐小时预报", padding=10)
        self.hourly_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(self.hourly_frame, text="输入城市查询逐小时天气").pack()

    def _show_hourly(self, hourly_data):
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.hourly_frame)
        container.pack()

        shown = 0
        now_hour = datetime.now().hour
        for h in hourly_data:
            try:
                hh = int(h["time"].split(":")[0])
            except (ValueError, IndexError):
                continue
            if hh < now_hour:
                continue
            if shown >= 8:
                break
            shown += 1

            col = ttk.Frame(container, padding=3)
            col.pack(side="left", padx=2)

            display = weather_to_display(h["description"])
            ttk.Label(col, text=h["time"], font=("Microsoft YaHei", 7)).pack()
            ttk.Label(col, text=display, font=("Microsoft YaHei", 12)).pack()

            color = temp_color(float(h["temperature"]))
            ttk.Label(col, text=f"{h['temperature']}°",
                      font=("Microsoft YaHei", 8, "bold"), foreground=color).pack()

    # ==================== 状态栏 ====================

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="就绪")
        status = ttk.Label(self.root, textvariable=self.status_var,
                           relief="sunken", anchor="w", padding=(5, 2))
        status.pack(side="bottom", fill="x")

    def _set_status(self, text):
        self.status_var.set(text)

    def _set_loading(self, loading):
        self._loading = loading
        if loading:
            self.search_btn.configure(state="disabled", text="查询中...")
            self._set_status("⏳ 正在查询...")
        else:
            self.search_btn.configure(state="normal", text="🔍 查询")

    # ==================== 核心逻辑 ====================

    def _on_search(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("提示", "请输入城市名")
            return
        if self._loading:
            return

        self._set_loading(True)
        thread = threading.Thread(target=self._fetch_and_show, args=(city,), daemon=True)
        thread.start()

    def _fetch_and_show(self, city):
        try:
            now = datetime.now()
            cached = self._cache.get(city)
            if cached and (now - cached[1]).seconds < 600:
                data = cached[0]
            else:
                raw = self.service._fetch(city)
                current = self.service.get_current(city)
                forecast = self.service.get_forecast(city)
                hourly = self.service.get_hourly(city)
                data = (city, current, forecast, hourly)
                self._cache[city] = (data, now)

            self.root.after(0, self._update_ui, *data)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, self._set_loading, False)

    def _update_ui(self, city, current, forecast, hourly):
        self._show_current(city, current)
        self._show_forecast(forecast)
        self._show_hourly(hourly)
        self._set_status(f"✅ 数据更新时间: {datetime.now().strftime('%H:%M:%S')}")

    def _show_error(self, error_msg):
        if "连接" in error_msg or "timeout" in error_msg.lower():
            messagebox.showwarning("网络错误", "无法连接到天气服务，请检查网络后重试")
            self._set_status("❌ 网络连接失败")
        else:
            messagebox.showerror("错误", f"查询失败：{error_msg}")
            self._set_status(f"❌ {error_msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()