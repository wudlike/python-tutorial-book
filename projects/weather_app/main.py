"""天气查询应用 —— 入口"""

import tkinter as tk
from weather_ui import WeatherApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()