"""天气查询应用 —— 数据显示与格式化
将原始天气数据转换为友好的显示格式
"""

WEATHER_MAP = {
    "Sunny":          ("晴", "☀️"),
    "Clear":          ("晴", "🌙"),
    "Partly cloudy":  ("多云", "⛅"),
    "Cloudy":         ("阴", "☁️"),
    "Overcast":       ("阴", "☁️"),
    "Mist":           ("雾", "🌫️"),
    "Fog":            ("雾", "🌫️"),
    "Light drizzle":  ("毛毛雨", "🌦️"),
    "Light rain":     ("小雨", "🌧️"),
    "Moderate rain":  ("中雨", "🌧️"),
    "Heavy rain":     ("大雨", "⛈️"),
    "Patchy rain possible": ("可能有雨", "🌦️"),
    "Light snow":     ("小雪", "🌨️"),
    "Moderate snow":  ("中雪", "❄️"),
    "Heavy snow":     ("大雪", "❄️"),
    "Snow":           ("雪", "❄️"),
    "Thunder":        ("雷暴", "⚡"),
    "Thundery outbreaks possible": ("可能有雷暴", "⛈️"),
}


def weather_to_display(english_desc):
    for key, (cn, emoji) in WEATHER_MAP.items():
        if key.lower() in english_desc.lower():
            return f"{emoji} {cn}"
    return english_desc


def temp_color(celsius):
    temp = float(celsius)
    if temp >= 35:
        return "#D32F2F"
    elif temp >= 28:
        return "#F57C00"
    elif temp >= 20:
        return "#388E3C"
    elif temp >= 10:
        return "#1976D2"
    elif temp >= 0:
        return "#0288D1"
    else:
        return "#7B1FA2"


def generate_summary(city, current, forecast):
    lines = [f"📍 {city} 当前天气"]
    lines.append(f"   温度: {current['temperature']}°C（体感 {current['feels_like']}°C）")
    lines.append(f"   天气: {weather_to_display(current['description'])}")
    lines.append(f"   湿度: {current['humidity']}%")
    lines.append(f"   风速: {current['wind_speed']} km/h")
    lines.append("")
    lines.append("📅 未来预报：")
    for f in forecast[:3]:
        lines.append(
            f"   {f['date']}  {f['min_temp']}~{f['max_temp']}°C  "
            f"{weather_to_display(f['description'])}"
        )
    return "\n".join(lines)