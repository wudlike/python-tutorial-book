## 17.2 数据处理与展示

API 返回的 JSON 数据是原始的、结构化的信息，需要经过"翻译"才能变成用户看得懂的天气卡片。本节完成从原始数据到结构化展示的转换。

### 17.2.1 数据解析

从 wttr.in 返回的 JSON 中提取关键字段：

```python
def parse_current_weather(raw_data):
    """从原始 JSON 中解析当前天气"""
    current = raw_data["current_condition"][0]
    return {
        "temperature": current["temp_C"],
        "humidity": current["humidity"],
        "description": current["weatherDesc"][0]["value"],
        "wind_speed": current["windspeedKmph"],
        "feels_like": current["FeelsLikeC"],
        "pressure": current.get("pressure", "N/A"),
        "visibility": current.get("visibility", "N/A"),
    }
```

### 17.2.2 天气预报解析

```python
def parse_forecast(raw_data):
    """解析未来天气预报"""
    forecasts = []
    for day in raw_data["weather"]:
        forecasts.append({
            "date": day["date"],
            "max_temp": day["maxtempC"],
            "min_temp": day["mintempC"],
            "avg_temp": day["avgtempC"],
            "description": day["hourly"][4]["weatherDesc"][0]["value"],
        })
    return forecasts
```

### 17.2.3 天气图标映射

将英文天气描述映射为直观的中文和 emoji：

```python
WEATHER_MAP = {
    "Sunny":        ("晴", "☀️"),
    "Clear":        ("晴", "🌙"),
    "Partly cloudy":("多云", "⛅"),
    "Cloudy":       ("阴", "☁️"),
    "Overcast":     ("阴", "☁️"),
    "Mist":         ("雾", "🌫️"),
    "Fog":          ("雾", "🌫️"),
    "Light rain":   ("小雨", "🌧️"),
    "Moderate rain":("中雨", "🌧️"),
    "Heavy rain":   ("大雨", "⛈️"),
    "Light snow":   ("小雪", "🌨️"),
    "Snow":         ("雪", "❄️"),
    "Thunder":      ("雷暴", "⚡"),
}

def weather_to_display(english_desc):
    """将英文天气描述转为中文 + emoji"""
    for key, (cn, emoji) in WEATHER_MAP.items():
        if key.lower() in english_desc.lower():
            return f"{emoji} {cn}"
    return english_desc  # 未匹配则原样返回
```

### 17.2.4 温度颜色算法

根据温度高低显示不同颜色，让用户一眼看出冷暖：

```python
def temp_color(celsius):
    """根据温度返回对应颜色"""
    temp = float(celsius)
    if temp >= 35:    return "#D32F2F"  # 红色——酷热
    elif temp >= 28:  return "#F57C00"  # 橙色——炎热
    elif temp >= 20:  return "#388E3C"  # 绿色——舒适
    elif temp >= 10:  return "#1976D2"  # 蓝色——凉爽
    elif temp >= 0:   return "#0288D1"  # 深蓝——寒冷
    else:             return "#7B1FA2"  # 紫色——冰冻
```

### 17.2.5 生成天气摘要文本

将解析后的数据组合成一段人类可读的摘要：

```python
def generate_summary(city, current_weather, forecast):
    """生成天气摘要文本"""
    lines = [f"📍 {city} 当前天气"]
    lines.append(f"   温度: {current_weather['temperature']}°C"
                 f"（体感 {current_weather['feels_like']}°C）")
    lines.append(f"   天气: {weather_to_display(current_weather['description'])}")
    lines.append(f"   湿度: {current_weather['humidity']}%")
    lines.append(f"   风速: {current_weather['wind_speed']} km/h")
    lines.append("")
    lines.append("📅 未来预报：")
    for f in forecast[:3]:
        lines.append(f"   {f['date']}  {f['min_temp']}~{f['max_temp']}°C  "
                     f"{weather_to_display(f['description'])}")
    return "\n".join(lines)
```

> 💡 **完整代码**：`projects/weather_app/weather_display.py`

### 17.2.6 命令行版本——先验证数据再上界面

在进入 GUI 开发之前，先用命令行测试所有功能是否正常：

```python
if __name__ == "__main__":
    city = input("请输入城市名（拼音或中文）: ").strip()
    if not city:
        city = "Beijing"

    try:
        raw = WeatherService.fetch_weather(city)
        current = parse_current_weather(raw)
        forecast = parse_forecast(raw)
        print(generate_summary(city, current, forecast))
    except Exception as e:
        print(f"❌ 出错: {e}")
```

这种"先命令行验证、再封装界面"的开发流程是 Python 项目的最佳实践——分离数据逻辑和界面逻辑，每一步都可以独立测试。