## 17.4 异常处理与用户体验

一个优秀的应用不仅要"功能正确"，还要"体验友好"。本节从异常处理、加载状态、缓存策略、错误恢复等角度，全面提升天气应用的健壮性和用户体验。

### 17.4.1 加载状态的视觉反馈

网络请求需要时间（通常 1~3 秒），这期间用户不应该对着空白的界面发呆。给出及时的视觉反馈：

```python
def _on_search(self):
    city = self.city_var.get().strip()
    if not city:
        messagebox.showwarning("提示", "请输入城市名")
        return

    # 显示加载状态
    self._set_loading(True)
    self._set_status("正在查询天气...")

    # 在后台线程中执行网络请求（避免界面卡顿）
    import threading
    thread = threading.Thread(target=self._fetch_and_show, args=(city,), daemon=True)
    thread.start()
```

多线程是 GUI 程序的关键技巧——网络请求放在后台线程中执行，主线程继续响应用户操作（如移动窗口、点击按钮），界面不会"卡死"：

```python
def _fetch_and_show(self, city):
    """在后台线程中获取数据并更新界面"""
    try:
        raw = WeatherService.fetch_weather(city)
        current = parse_current_weather(raw)
        forecast = parse_forecast(raw)
        hourly = parse_hourly(raw)

        # 切回主线程更新 UI
        self.root.after(0, self._update_ui, city, current, forecast, hourly)
    except Exception as e:
        self.root.after(0, self._show_error, str(e))
    finally:
        self.root.after(0, self._set_loading, False)
```

`root.after(0, callback)` 是 Tkinter 的线程安全方法——将回调函数调度到主线程的事件循环中执行。**绝对不能**在后台线程中直接操作 Tkinter 控件，否则会导致崩溃。

### 17.4.2 友好的错误处理

不同错误给出不同级别的提示：

```python
def _show_error(self, error_msg):
    """根据错误类型显示不同提示"""
    if "连接" in error_msg or "timeout" in error_msg.lower():
        messagebox.showwarning("网络错误", "无法连接到天气服务，请检查网络后重试")
        self._set_status("❌ 网络连接失败")
    elif "未找到" in error_msg:
        messagebox.showinfo("提示", f"没有找到城市"{self.city_var.get()}"的天气数据")
        self._set_status("❌ 城市未找到")
    else:
        messagebox.showerror("错误", f"查询失败：{error_msg}")
        self._set_status(f"❌ {error_msg}")
```

### 17.4.3 本地缓存——减少 API 调用

wttr.in 虽然没有 API Key 限制，但频繁请求仍不礼貌。加一个简单的内存缓存：

```python
from datetime import datetime, timedelta

class WeatherCache:
    def __init__(self, ttl_minutes=10):
        self._cache = {}
        self._ttl = timedelta(minutes=ttl_minutes)

    def get(self, city):
        if city in self._cache:
            data, timestamp = self._cache[city]
            if datetime.now() - timestamp < self._ttl:
                return data
        return None

    def set(self, city, data):
        self._cache[city] = (data, datetime.now())

    def clear(self):
        self._cache.clear()
```

使用缓存后，用户连续查询同一城市时，10 分钟内直接返回缓存数据，响应几乎瞬间完成。

### 17.4.4 状态栏——让用户知道"发生了什么"

底部的状态栏持续反馈当前状态：

```python
def _set_status(self, text):
    self.status_var.set(text)

def _set_loading(self, loading):
    if loading:
        # 查询按钮变灰，防止重复点击
        self.search_btn.configure(state="disabled", text="查询中...")
    else:
        self.search_btn.configure(state="normal", text="🔍 查询")
```

### 17.4.5 用户体验优化清单

| 优化点 | 实现方式 | 用户感知 |
|--------|----------|----------|
| 加载动画 | 查询时显示"查询中..." | 知道程序在工作，不会焦虑 |
| 输入校验 | 空输入时弹窗提示 | 不会提交无效请求 |
| 回车触发 | 绑定 `<Return>` 事件 | 不用鼠标也能操作 |
| 防重复点击 | 查询中禁用按钮 | 避免同时发起多个请求 |
| 数据缓存 | 内存缓存 10 分钟 | 同一城市秒开 |
| 错误分级 | info/warning/error 不同对话框 | 知道问题严重程度 |
| 默认城市 | 启动时自动查"北京" | 打开应用就能看到天气 |
| 窗口大小固定 | `resizable(False, False)` | 避免布局被拖乱 |

### 17.4.6 天气应用的打包发布

和第 16 章一样，使用 PyInstaller 打包：

```bash
cd projects/weather_app
pyinstaller --onefile --windowed --name="天气查询" --icon=weather.ico main.py
```

打包前别忘了在代码中处理数据库/文件路径的问题——使用 `sys.argv[0]` 来确定 exe 所在目录，而不是相对路径。

### 实战练习

1. 为天气应用添加"收藏城市"功能——用户可以将常用城市加入收藏列表，方便快速切换。收藏数据持久化保存到本地 JSON 文件中。

2. 添加"天气预警"功能——每天定时检查收藏城市的天气，如果未来 24 小时内有暴雨/大风/高温预警，通过系统通知提醒用户（参考 15.4 节）。

3. 优化 weather_service.py，增加"API 降级"逻辑——当 wttr.in 不可用时，自动切换到备用 API（如 OpenWeatherMap），确保应用的高可用性。