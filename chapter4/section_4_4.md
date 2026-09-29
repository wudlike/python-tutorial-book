## 4.4 综合案例——修仙渡劫模拟器

本章学完了条件判断、循环和循环控制三大利器，是时候把它们组合起来完成一个完整的程序了。下面这个"修仙渡劫模拟器"将依次用到 `if-elif-else`、`for`、`while`、`break` 和 `continue`，你可以在阅读代码时逐一辨认它们的出场位置。

### 4.4.1 游戏设定

你是一名初入道途的修仙者，目标是从"凡人"一路突破到"大乘"。你需要通过修炼积累灵气，在灵气充盈时选择渡劫——渡劫成功则突破境界，失败则损失灵气重头再来。连败三次则道心崩溃，游戏结束。

| 境界 | 渡劫所需灵气 | 天雷道数 |
|:----:|:----------:|:------:|
| 凡人 → 筑基 | 50 | 3 |
| 筑基 → 金丹 | 80 | 4 |
| 金丹 → 元婴 | 120 | 5 |
| 元婴 → 化神 | 180 | 6 |
| 化神 → 大乘 | 260 | 7 |

每道天雷有 40% 的概率劈中你——劈中扣灵气，躲过则安然无恙。渡劫结束时灵气仍为正数即为成功。

### 4.4.2 完整代码

```python
import random

# ===== 游戏初始化 =====
realms = ["凡人", "筑基", "金丹", "元婴", "化神", "大乘"]
realm_index = 0              # 当前境界索引
qi = 20                      # 当前灵气值
required_qi = [50, 80, 120, 180, 260]
lightning_count = [3, 4, 5, 6, 7]

fail_streak = 0              # 连续渡劫失败次数
max_fail = 3                 # 允许的最大连续失败次数

# ===== 游戏主循环 =====
while realm_index < len(realms) - 1:
    print("\n" + "=" * 40)
    print(f"当前境界：{realms[realm_index]}")
    print(f"灵气值：{qi} / {required_qi[realm_index]}")
    print(f"连续失败次数：{fail_streak} / {max_fail}")

    # 检查是否道心崩溃
    if fail_streak >= max_fail:
        print("\n☠️  连败三次，道心崩溃……修仙之路到此为止。")
        break                          # ← break: 终止游戏

    # 玩家选择行动
    print("\n请选择行动：")
    print("  1. 修炼（随机获得 10-30 灵气）")
    print("  2. 渡劫（尝试突破境界）")
    print("  3. 休息（恢复 5-15 灵气）")
    print("  0. 退出游戏")
    choice = input("输入选项：")

    # ===== 条件判断：处理玩家选择 =====
    if choice == "0":
        print("修仙者退出了修炼……")
        break                          # ← break: 退出游戏

    elif choice == "1":
        gain = random.randint(10, 30)
        qi += gain
        print(f"🧘 你闭关修炼，获得 {gain} 点灵气！")

    elif choice == "2":
        if qi < required_qi[realm_index]:
            print(f"❌ 灵气不足！需要 {required_qi[realm_index]} 点灵气才能渡劫。")
            continue                   # ← continue: 跳过本轮，回到选择菜单

        print(f"\n⚡ 开始渡劫——突破至【{realms[realm_index + 1]}】！")
        tribulation_qi = qi            # 记录渡劫前的灵气

        # for 循环：逐道天雷
        for strike in range(1, lightning_count[realm_index] + 1):
            hit = random.random() < 0.4
            if hit:
                damage = random.randint(5, 15)
                qi -= damage
                print(f"  第 {strike} 道天雷劈中！灵气 -{damage}（剩余 {qi}）")
            else:
                print(f"  第 {strike} 道天雷落空！你躲过一劫（灵气 {qi}）")

            if qi <= 0:
                print("💀 灵气耗尽，渡劫失败！")
                break                  # ← break: 灵气耗尽，终止天雷循环

        # 渡劫结果判断
        if qi > 0:
            realm_index += 1
            fail_streak = 0
            print(f"\n🎉 渡劫成功！你已突破至【{realms[realm_index]}】！")
        else:
            fail_streak += 1
            qi = tribulation_qi // 2   # 失败后灵气减半
            print(f"\n😞 渡劫失败……灵气折半，继续修炼吧。")

    elif choice == "3":
        rest = random.randint(5, 15)
        qi += rest
        print(f"🛌 你静心休养，恢复 {rest} 点灵气。")

    else:
        print("⚠️  无效的选择，请重新输入。")
        continue                       # ← continue: 无效输入，跳过后续判断

    # 灵气上限保护
    if qi > 300:
        qi = 300
        print("⚠️  灵气已达到上限（300）。")

# ===== 游戏结束 =====
if realm_index == len(realms) - 1:
    print("\n" + "=" * 40)
    print(f"🏆 恭喜！你已突破至【大乘】境界，飞升在即！")
    print("=" * 40)
```

### 4.4.3 知识点对照

运行这个游戏，你会看到本章的每个知识点都在发挥作用：

| 知识点 | 出现位置 | 作用 |
|:------|:-----|:-----|
| `if-elif-else` | 处理玩家选项（`choice == "0"/"1"/"2"/"3"`） | 根据输入走不同分支 |
| `while` 循环 | 游戏主循环 | 只要没通关也没失败，就持续运行 |
| `for` 循环 | 渡劫时逐道天雷 | 遍历固定次数（天雷道数） |
| `break` | 道心崩溃退出 / 退出选项 / 灵气耗尽 | 在三种不同场景下终止循环 |
| `continue` | 灵气不足 / 无效输入 | 跳过本轮，回到选择菜单 |
| 比较运算符 | `>=` `>` `==` `<=` | 判断境界、灵气、失败次数等各种条件 |
| 逻辑运算符 | `random.random() < 0.4` | 天雷击中概率判断 |

### 4.4.4 试一试：修改游戏

理解代码后，尝试做以下修改来加深理解：

1. **增加奖励机制**：修炼时 10% 概率触发"顿悟"，额外获得 20 点灵气。提示：在 `elif choice == "1"` 分支中加一层 `if` 判断。

2. **调整难度**：修改天雷伤害范围（原 5~15）、失败后灵气折损比例（原 1/2）、或添加"渡劫时 20% 概率触发心魔，伤害翻倍"。

3. **记录历史**：用列表记录每次渡劫的结果（成功/失败），渡劫结束后打印"修仙履历"。