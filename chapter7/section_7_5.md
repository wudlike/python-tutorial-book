## 7.5 案例：学生管理系统——OOP 综合实战

前面四节分别讲了类与对象、属性与方法、继承与多态、特殊方法。现在我们用一个完整的案例——**学生管理系统**——把这些知识点串起来，看看面向对象编程在真实场景中是如何组织代码的。

### 7.5.1 需求分析

我们要设计一个学生管理系统，支持以下功能：
1. **添加学生**：录入姓名、年龄和初始成绩
2. **查看学生**：列出所有学生信息
3. **查找学生**：根据姓名查找特定学生
4. **修改成绩**：给某位学生的某门课录入或更新成绩
5. **成绩排名**：按平均分从高到低排列所有学生
6. **优秀学生评选**：自动评选平均分 90 分以上的"优秀学生"

一个学生可能包含多门课程的成绩——这个系统需要足够灵活，允许不同学生选修不同的课程组合。

### 7.5.2 设计思路：先找类，再找关系

面向对象编程的第一步不是写代码，而是**识别领域中的实体以及它们之间的关系**。在这个系统中，最核心的实体有两个：

- **Student（学生）**：拥有姓名、年龄、多门课程的成绩，能计算平均分、判断是否优秀
- **StudentManager（学生管理器）**：管理一组学生，负责增删查改、排名、评选等操作

它们的关系是"一对多"（1 个管理器包含多个学生）——这正是**组合**（Composition）的典型场景：管理器拥有一个学生列表，负责协调学生之间的交互。

### 7.5.3 第一步：定义 Student 类

先定义最基础的学生类，让它具备基本的数据存储和展示能力：

```python
class Student:
    """学生类——代表一个学生的全部信息"""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.scores = {}          # 字典：课程名 → 成绩

    def add_or_update_score(self, subject, score):
        """添加或更新一门课的成绩"""
        if 0 <= score <= 100:
            self.scores[subject] = score
            print(f"{self.name} 的 {subject} 成绩已更新为 {score}")
        else:
            print(f"错误：成绩必须在 0-100 之间，收到 {score}")

    def get_average_score(self):
        """计算平均分——没有成绩时返回 0"""
        if not self.scores:
            return 0
        return sum(self.scores.values()) / len(self.scores)

    def is_excellent(self):
        """判断是否为优秀学生（平均分 90 以上）"""
        return self.get_average_score() >= 90

    def __str__(self):
        """学生信息概览——面向用户的友好输出"""
        avg = self.get_average_score()
        level = "优秀" if self.is_excellent() else "普通"
        course_count = len(self.scores)
        return f"{self.name}（{self.age}岁）| {course_count}门课 | 平均分 {avg:.1f} | {level}"

    def detail(self):
        """详细成绩单——包含每门课的成绩"""
        lines = [f"姓名：{self.name}", f"年龄：{self.age}"]
        if self.scores:
            lines.append("成绩单：")
            for subject, score in self.scores.items():
                bar = "█" * (score // 10)      # 用方块做简易可视化
                lines.append(f"  {subject}：{score} 分 {bar}")
            lines.append(f"  平均分：{self.get_average_score():.1f}")
        else:
            lines.append("成绩单：暂无成绩")
        return "\n".join(lines)
```

这个类的设计有几个值得关注的点：

- `scores` 用字典存储，键是课程名、值是分数。为什么不用列表？因为"语文=90"比"第0个是90"更有语义，而且不同学生可以用不同的课程组合
- `add_or_update_score` 包含了输入校验（0-100 分范围），保证了数据的合法性——这种"防御性编程"的习惯应该在写每个方法时都带上
- `__str__` 提供概览信息，`detail()` 提供详细成绩单——两者分工明确，前者用于批量列表展示，后者用于单个学生的深入查看
- `get_average_score()` 处理了没有成绩的边界情况（返回 0 而不是除以 0 报错）

### 7.5.4 第二步：定义 StudentManager 类

管理器类负责协调所有学生的操作，是用户交互的唯一入口：

```python
class StudentManager:
    """学生管理器——管理一组学生的增删查改等操作"""

    def __init__(self):
        self.students = []          # 存储所有学生对象的列表

    def add_student(self, name, age):
        """添加一名新学生"""
        for s in self.students:
            if s.name == name:
                print(f"错误：学生 {name} 已存在")
                return
        student = Student(name, age)
        self.students.append(student)
        print(f"学生 {name} 添加成功")

    def find_student(self, name):
        """按姓名查找学生——返回 Student 对象或 None"""
        for s in self.students:
            if s.name == name:
                return s
        return None

    def show_all(self):
        """列出所有学生信息概览"""
        if not self.students:
            print("暂无学生信息")
            return
        print(f"\n{'='*50}")
        print(f"学生列表（共 {len(self.students)} 人）")
        print(f"{'='*50}")
        for s in self.students:
            print(s)          # 触发 __str__

    def show_detail(self, name):
        """查看某个学生的详细成绩单"""
        student = self.find_student(name)
        if student:
            print(f"\n{student.detail()}")
        else:
            print(f"未找到学生：{name}")

    def update_score(self, name, subject, score):
        """更新学生的成绩"""
        student = self.find_student(name)
        if student:
            student.add_or_update_score(subject, score)
        else:
            print(f"未找到学生：{name}")

    def ranking(self):
        """按平均分从高到低排名"""
        if not self.students:
            print("暂无学生信息")
            return
        ranked = sorted(self.students, key=lambda s: s.get_average_score(), reverse=True)
        print(f"\n{'='*50}")
        print("成绩排名")
        print(f"{'='*50}")
        for i, s in enumerate(ranked, 1):
            medal = ["🏅", "🥈", "🥉"][i-1] if i <= 3 else f"{i:2d}."
            print(f"{medal} {s}")

    def excellent_students(self):
        """评选优秀学生（平均分 90 以上）"""
        excellent = [s for s in self.students if s.is_excellent()]
        if not excellent:
            print("暂无优秀学生（平均分需达到 90 分）")
            return
        print(f"\n{'='*50}")
        print(f"优秀学生（共 {len(excellent)} 人）")
        print(f"{'='*50}")
        for s in excellent:
            print(f"  {s.name}——平均分 {s.get_average_score():.1f}")
```

管理器的设计原则是**职责清晰**：
- 管理器不关心学生内部的成绩如何存储——那是 `Student` 类的责任
- 学生不关心排名和筛选——那是 `StudentManager` 类的责任
- 两者通过清晰的接口（`find_student` 返回 `Student` 对象，然后调用 `Student` 的方法）来协作

### 7.5.5 第三步：组装交互界面

最后用一个简单的命令行菜单把管理器"激活"，让用户可以直接操作：

```python
def main():
    manager = StudentManager()

    # 预设一些示例数据，方便测试
    manager.add_student("小明", 18)
    manager.add_student("小红", 17)
    manager.add_student("小刚", 19)
    manager.add_student("小李", 18)
    manager.update_score("小明", "语文", 88)
    manager.update_score("小明", "数学", 95)
    manager.update_score("小明", "英语", 73)
    manager.update_score("小红", "语文", 92)
    manager.update_score("小红", "数学", 87)
    manager.update_score("小红", "英语", 96)
    manager.update_score("小刚", "语文", 76)
    manager.update_score("小刚", "数学", 82)
    manager.update_score("小刚", "英语", 69)
    manager.update_score("小李", "语文", 94)
    manager.update_score("小李", "数学", 97)
    manager.update_score("小李", "英语", 91)

    while True:
        print(f"\n{'='*50}")
        print("学生管理系统")
        print(f"{'='*50}")
        print("1. 查看所有学生")
        print("2. 查看学生详情")
        print("3. 添加学生")
        print("4. 录入/修改成绩")
        print("5. 成绩排名")
        print("6. 优秀学生评选")
        print("0. 退出")
        print(f"{'='*50}")

        choice = input("请选择操作：").strip()

        if choice == "1":
            manager.show_all()

        elif choice == "2":
            name = input("请输入学生姓名：").strip()
            manager.show_detail(name)

        elif choice == "3":
            name = input("请输入姓名：").strip()
            try:
                age = int(input("请输入年龄：").strip())
                manager.add_student(name, age)
            except ValueError:
                print("错误：年龄必须是整数")

        elif choice == "4":
            name = input("请输入学生姓名：").strip()
            subject = input("请输入课程名称：").strip()
            try:
                score = int(input("请输入成绩（0-100）：").strip())
                manager.update_score(name, subject, score)
            except ValueError:
                print("错误：成绩必须是整数")

        elif choice == "5":
            manager.ranking()

        elif choice == "6":
            manager.excellent_students()

        elif choice == "0":
            print("再见！")
            break

        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()
```

### 7.5.6 知识点回顾——这个案例教会了你什么

| 知识点 | 在案例中的体现 |
|:-------|:--------------|
| **类与对象** | `Student` 和 `StudentManager` 是两个独立的类，各有自己的职责 |
| **`__init__`** | 两个类都用 `__init__` 初始化属性（姓名、成绩字典、学生列表） |
| **实例方法** | `get_average_score()`、`is_excellent()`、`detail()` 等操作实例数据 |
| **`__str__`** | `Student.__str__` 让 `print(s)` 输出有意义的概览信息 |
| **字典操作** | `scores` 用字典存储，灵活支持不同的课程组合 |
| **组合关系** | `StudentManager` 包含 `Student` 列表，通过 `find_student` 获取对象后调用其方法 |
| **`lambda` + `sorted`** | 排名功能用 `lambda s: s.get_average_score()` 作为排序键 |
| **列表推导式** | 优秀学生筛选用 `[s for s in ... if s.is_excellent()]` |
| **输入校验** | 成绩范围检查、年龄类型检查、重名检查——防御性编程 |
| **`__name__`** | `if __name__ == "__main__"` 让文件既可运行也可被导入 |

### 7.5.7 实战练习

1. 为 `Student` 类添加一个 `__lt__` 方法，让学生对象可以直接用 `<` 比较（按平均分比较）。然后用 `sorted(students)` 对学生列表排序，验证结果。

2. 为 `StudentManager` 类添加一个 `remove_student(name)` 方法，支持按姓名删除学生。删除时需要确认学生存在，如果不存在应给出提示。

3. 为 `StudentManager` 类添加一个 `statistics()` 方法，统计并输出以下信息：学生总人数、全部学生所有科目的平均分、最高平均分和最低平均分的学生姓名及分数（提示：用 `max()` 和 `min()` 配合 `lambda`）。