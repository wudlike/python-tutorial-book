## 15.4 系统监控脚本——让服务器"会说话"

服务器宕机了没人知道、磁盘快满了没预警、某个进程 CPU 飙到 99%……这些都是运维中的经典"灾难"。系统监控脚本的作用就是在问题发生时**第一时间通知你**，而不是等到用户投诉了才发现。

Python 的 `psutil`（process and system utilities）库提供了跨平台的系统监控能力——CPU、内存、磁盘、网络、进程，一个库全部搞定。本节将用它构建一个完整的服务器监控系统。

### 15.4.1 `psutil` 基础——系统指标的"万用表"

```python
# pip install psutil

import psutil

# CPU
print(f"CPU 核心数: {psutil.cpu_count()}（逻辑: {psutil.cpu_count(logical=False)} 物理核）")
print(f"CPU 使用率: {psutil.cpu_percent(interval=1)}%")
print(f"每个核心: {psutil.cpu_percent(interval=0.5, percpu=True)}")

# 内存
mem = psutil.virtual_memory()
print(f"\n总内存: {mem.total / (1024**3):.1f} GB")
print(f"已用:   {mem.used / (1024**3):.1f} GB ({mem.percent}%)")
print(f"可用:   {mem.available / (1024**3):.1f} GB")

# 磁盘
for part in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(part.mountpoint)
        print(f"\n磁盘 {part.device} ({part.mountpoint}):")
        print(f"  总容量: {usage.total / (1024**3):.1f} GB")
        print(f"  已用:   {usage.used / (1024**3):.1f} GB ({usage.percent}%)")
    except PermissionError:
        pass

# 网络
net_io = psutil.net_io_counters()
print(f"\n网络 — 发送: {net_io.bytes_sent / (1024**2):.1f} MB | "
      f"接收: {net_io.bytes_recv / (1024**2):.1f} MB")

# 启动时间
from datetime import datetime
boot_time = datetime.fromtimestamp(psutil.boot_time())
print(f"\n系统启动于: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")

# 当前用户
users = psutil.users()
for user in users:
    print(f"登录用户: {user.name} @ {user.host or '本地'}")
```

### 15.4.2 进程管理——找到"捣乱"的进程

```python
import psutil

# 列出 CPU 占用最高的 5 个进程
print("CPU 占用 TOP 5:")
processes = []
for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
    try:
        processes.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

top_cpu = sorted(processes, key=lambda p: p["cpu_percent"] or 0, reverse=True)[:5]
for p in top_cpu:
    print(f"  PID {p['pid']:6d} | {p['name']:20s} | "
          f"CPU: {p['cpu_percent']:5.1f}% | MEM: {p['memory_percent']:5.1f}%")

# 查找特定进程
def find_process(name_pattern):
    """根据名称查找进程"""
    found = []
    for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        try:
            if name_pattern.lower() in proc.info["name"].lower():
                found.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return found

python_procs = find_process("python")
print(f"\n找到 {len(python_procs)} 个 Python 进程:")
for p in python_procs:
    cmd = " ".join(p["cmdline"][:3]) if p["cmdline"] else "(无命令行)"
    print(f"  PID {p['pid']}: {cmd}")

# 安全终止进程
def kill_process_safe(pid):
    """安全地终止进程——先尝试正常退出，不行再强制"""
    try:
        proc = psutil.Process(pid)
        print(f"正在终止 {proc.name()} (PID: {pid})...")
        proc.terminate()                         # SIGTERM —— 礼貌地请进程退出
        proc.wait(timeout=5)                     # 等 5 秒
        print(f"  ✅ 进程已正常退出")
    except psutil.TimeoutExpired:
        print(f"  ⚠️ 进程未响应，强制终止...")
        proc.kill()                               # SIGKILL —— 强制杀死
        print(f"  ✅ 进程已被强制终止")
    except psutil.NoSuchProcess:
        print(f"  ℹ️ 进程已不存在")
```

### 15.4.3 构建完整的监控系统

将检测逻辑、报警阈值和通知机制组合成一个可运行的监控守护进程：

```python
import psutil
import time
import json
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    """系统监控器——定期检查并报警"""

    def __init__(self, thresholds=None, log_file="monitor.log"):
        self.thresholds = thresholds or {
            "cpu": 80,            # CPU 使用率超过 80% 报警
            "memory": 85,         # 内存使用率超过 85% 报警
            "disk": 90,           # 磁盘使用率超过 90% 报警
        }
        self.log_file = Path(log_file)
        self.alerts = []

    def check(self):
        """执行一次全面检查，返回报警列表"""
        alerts = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # CPU 检查
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.thresholds["cpu"]:
            alerts.append(f"[{timestamp}] ⚠️ CPU 使用率过高: {cpu_percent}% "
                          f"(阈值: {self.thresholds['cpu']}%)")

        # 内存检查
        mem = psutil.virtual_memory()
        if mem.percent > self.thresholds["memory"]:
            alerts.append(f"[{timestamp}] ⚠️ 内存使用率过高: {mem.percent}% "
                          f"(阈值: {self.thresholds['memory']}%)")

        # 磁盘检查
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                if usage.percent > self.thresholds["disk"]:
                    alerts.append(
                        f"[{timestamp}] ⚠️ 磁盘空间不足: {part.device} "
                        f"({part.mountpoint}) 已用 {usage.percent}% "
                        f"(阈值: {self.thresholds['disk']}%)"
                    )
            except PermissionError:
                pass

        # 记录
        summary = (
            f"[{timestamp}] CPU: {cpu_percent}% | MEM: {mem.percent}% | "
            f"警报: {len(alerts)}"
        )
        self._log(summary)

        for alert in alerts:
            self._log(alert)

        return alerts

    def _log(self, message):
        """写入日志文件"""
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def run(self, interval=60, alert_callback=None):
        """持续监控——每隔 interval 秒检查一次"""
        print(f"🖥️ 系统监控已启动（间隔: {interval}s）")
        print(f"   报警阈值: {self.thresholds}")
        print(f"   日志文件: {self.log_file}")

        try:
            while True:
                alerts = self.check()

                # 如果有报警且设置了回调函数，调用它
                if alerts and alert_callback:
                    alert_callback(alerts)

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 监控已停止")

# ==================== 使用示例 ====================
def send_alert(alerts):
    """报警回调——实际项目中这里可以发邮件、发微信等"""
    print("\n" + "=" * 60)
    print("🚨 系统报警！")
    for alert in alerts:
        print(f"  {alert}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    monitor = SystemMonitor(
        thresholds={"cpu": 70, "memory": 80, "disk": 85},
        log_file="system_monitor.log"
    )
    monitor.run(interval=10, alert_callback=send_alert)
```

### 15.4.4 生成监控报告

定期生成一份"系统健康报告"（HTML 格式），可以配合 15.2 节的邮件发送功能自动推送：

```python
import psutil
from datetime import datetime

def generate_health_report():
    """生成系统健康报告（HTML）"""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    boot = datetime.fromtimestamp(psutil.boot_time())

    # 颜色判定
    def color(value, warn=70, crit=90):
        if value >= crit: return "#f44336"     # 红色-严重
        if value >= warn: return "#ff9800"      # 橙色-警告
        return "#4caf50"                         # 绿色-正常

    report = f"""
    <div style="font-family: 'Microsoft YaHei'; max-width: 650px; margin: 0 auto;">
        <h2 style="color: #1565C0;">📊 系统健康报告</h2>
        <p style="color: #888;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #f5f5f5;">
                <th style="padding: 10px; text-align: left;">指标</th>
                <th style="padding: 10px; text-align: left;">当前值</th>
                <th style="padding: 10px; text-align: left;">状态</th>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">CPU 使用率</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{cpu}%</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <span style="color:{color(cpu)}; font-weight:bold;">
                        {"● 正常" if cpu < 70 else "● 偏高" if cpu < 90 else "● 危险"}
                    </span>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">内存使用率</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{mem.percent}%</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <span style="color:{color(mem.percent)}; font-weight:bold;">
                        {"● 正常" if mem.percent < 70 else "● 偏高" if mem.percent < 90 else "● 危险"}
                    </span>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">磁盘使用率</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{disk.percent}%</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <span style="color:{color(disk.percent)}; font-weight:bold;">
                        {"● 正常" if disk.percent < 70 else "● 偏高" if disk.percent < 90 else "● 危险"}
                    </span>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">网络发送</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;" colspan="2">
                    {net.bytes_sent / (1024**3):.2f} GB
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">系统运行时间</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;" colspan="2">
                    {datetime.now() - boot}
                </td>
            </tr>
        </table>

        <p style="color: #888; font-size: 12px; margin-top: 20px;">
            此报告由 Python 系统监控脚本自动生成
        </p>
    </div>
    """
    return report

# html_report = generate_health_report()
# 可以将 html_report 作为邮件正文发送（参考 15.2 节）
```

### 15.4.5 实战练习

1. 扩展 `SystemMonitor` 类，增加"网络流量异常检测"功能——如果 `psutil.net_io_counters()` 的接收或发送速率超过正常水平的 3 倍标准差（基于最近 10 次采样），触发报警。

2. 编写一个"进程看门狗"（Watchdog）——监视指定的进程名称（如 `nginx`、`mysql`），如果进程意外退出，自动重启它，并记录重启日志。

3. 将系统监控器、健康报告生成和邮件发送（15.2 节）串联起来：监控器在检测到异常时自动生成 HTML 健康报告并通过邮件发送给管理员。每天早 9 点也例行发送一份健康报告。