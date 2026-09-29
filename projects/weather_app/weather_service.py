"""天气查询应用 —— 天气服务层
封装 wttr.in API，提供天气数据获取功能
"""

import requests
from datetime import datetime


class WeatherService:
    BASE_URL = "https://wttr.in"

    @staticmethod
    def _fetch(city):
        url = f"{WeatherService.BASE_URL}/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_current(city):
        raw = WeatherService._fetch(city)
        current = raw["current_condition"][0]
        return {
            "temperature": current["temp_C"],
            "humidity": current["humidity"],
            "description": current["weatherDesc"][0]["value"],
            "wind_speed": current["windspeedKmph"],
            "wind_dir": current.get("winddir16Point", "N/A"),
            "feels_like": current["FeelsLikeC"],
            "pressure": current.get("pressure", "N/A"),
            "visibility": current.get("visibility", "N/A"),
            "uv_index": current.get("uvIndex", "N/A"),
        }

    @staticmethod
    def get_forecast(city, days=3):
        raw = WeatherService._fetch(city)
        forecasts = []
        for day in raw["weather"][:days]:
            forecasts.append({
                "date": day["date"],
                "max_temp": day["maxtempC"],
                "min_temp": day["mintempC"],
                "avg_temp": day["avgtempC"],
                "description": day["hourly"][4]["weatherDesc"][0]["value"],
                "sun_hour": day["astronomy"][0].get("sunshine_hours", "N/A"),
            })
        return forecasts

    @staticmethod
    def get_hourly(city):
        raw = WeatherService._fetch(city)
        hourly = []
        today = raw["weather"][0]["hourly"]
        for h in today:
            time_str = datetime.fromtimestamp(
                int(h.get("time", 0)) / 1000
            ).strftime("%H:%M") if h.get("time") else "N/A"
            hourly.append({
                "time": time_str,
                "temperature": h["tempC"],
                "description": h["weatherDesc"][0]["value"],
                "chance_of_rain": h.get("chanceofrain", "0"),
            })
        return hourly

    @staticmethod
    def get_city_suggestions(query):
        try:
            url = f"{WeatherService.BASE_URL}/{query}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            area = data.get("nearest_area", [{}])[0]
            city_name = area.get("areaName", [{}])[0].get("value", query)
            country = area.get("country", [{}])[0].get("value", "")
            return [f"{city_name}, {country}"]
        except Exception:
            return [query]