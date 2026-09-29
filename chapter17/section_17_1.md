## 17.1 API 接口调用

天气数据不会凭空产生——它来自专业的天气数据服务商。我们通过 HTTP API 获取实时天气信息，这是现代应用最常见的"获取外部数据"方式。

### 17.1.1 选择天气 API

主流的免费天气 API 包括：

| API | 特点 | 是否需要注册 |
|-----|------|-------------|
| OpenWeatherMap | 数据全面，支持全球城市 | 需要 API Key |
| 和风天气 | 国内城市数据准确，有免费额度 | 需要 API Key |
| wttr.in | 无需注册，直接 URL 访问 | 不需要 |
| 心知天气 | 中文友好，免费 400 次/小时 | 需要 API Key |

本章使用 **wttr.in** 作为演示，因为它不需要注册、不需要 Key，最简单的请求就是：`https://wttr.in/Beijing?format=j1`。

### 17.1.2 从 wttr.in 获取天气数据

```python
import requests

def fetch_weather(city):
    """从 wttr.in 获取指定城市的天气数据"""
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

返回的 JSON 结构如下（简化版）：

```json
{
  "current_condition": [{
    "temp_C": "22",
    "humidity": "65",
    "weatherDesc": [{"value": "Sunny"}],
    "windspeedKmph": "15",
    "FeelsLikeC": "20"
  }],
  "weather": [{
    "date": "2024-06-15",
    "avgtempC": "24",
    "hourly": [
      {"tempC": "20", "weatherDesc": [{"value": "Clear"}]},
      ...
    ]
  }]
}
```

### 17.1.3 封装天气服务类

把 API 调用封装成一个类，统一管理城市查询、错误处理和超时：

```python
# 完整代码见 projects/weather_app/weather_service.py

class WeatherService:
    BASE_URL = "https://wttr.in"

    @staticmethod
    def get_current(city):
        """获取当前天气 → 返回字典 {温度, 湿度, 天气描述, 风速, 体感温度}"""
        ...

    @staticmethod
    def get_forecast(city, days=3):
        """获取未来几天的天气预报 → 返回列表 [{日期, 最高温, 最低温, 天气}, ...]"""
        ...

    @staticmethod
    def get_hourly(city):
        """获取今天逐小时天气 → 返回列表 [{时间, 温度, 天气}, ...]"""
        ...

    @staticmethod
    def get_city_suggestions(query):
        """城市搜索建议——输入拼音或中文名，返回匹配的城市列表"""
        ...
```

> 💡 **完整代码**：`projects/weather_app/weather_service.py`

### 17.1.4 异常处理——网络请求的"安全带"

调用外部 API 可能遇到各种问题，必须做好异常处理：

```python
def safe_fetch(city):
    try:
        data = WeatherService.get_current(city)
        return data, None
    except requests.ConnectionError:
        return None, "网络连接失败，请检查网络设置"
    except requests.Timeout:
        return None, "请求超时，请稍后重试"
    except requests.HTTPError as e:
        return None, f"服务器错误 ({e.response.status_code})"
    except (KeyError, ValueError):
        return None, f"未找到城市"{city}"的天气数据"
```

每一种异常对应一种具体的失败原因，用户看到的不再是一串吓人的 traceback，而是通俗易懂的中文提示。

> 💡 **要点**：Python 中的异常处理就像开车时的安全气囊——正常情况下不触发，但一旦出了问题，它能保护程序不崩溃，同时给用户一个友好的反馈。这在任何需要调用外部服务的程序中都是**必须**的。