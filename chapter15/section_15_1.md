## 15.1 文件批量处理——告别手动操作

日常工作中充满了琐碎的文件操作：给 100 张照片批量重命名、把 50 个 Word 文档转换成 PDF、按日期整理下载文件夹……这些任务的特点是"规则明确但数量庞大"——正是自动化脚本的完美用武之地。

Python 的 `os`、`shutil` 和 `pathlib` 三个模块构成了文件自动化处理的基石。本节聚焦最实用的批量处理场景，每个场景都可以直接复制到你的项目中使用。

### 15.1.1 批量重命名——统一命名规则

最常见的需求之一：把一堆混乱的文件名改为统一的格式：

```python
import os

def batch_rename(directory, prefix="file", start_num=1, extension=None):
    """批量重命名文件——文件名格式化为 prefix_001.ext"""
    files = [f for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))]

    for i, old_name in enumerate(sorted(files), start=start_num):
        old_path = os.path.join(directory, old_name)
        _, ext = os.path.splitext(old_name)

        # 保留原扩展名，或使用指定的扩展名
        new_ext = extension if extension else ext
        new_name = f"{prefix}_{i:03d}{new_ext}"
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"  {old_name} → {new_name}")

    print(f"完成！共处理 {len(files)} 个文件")

# 使用示例：将所有照片重命名为 photo_001.jpg, photo_002.jpg...
# batch_rename("./photos", prefix="photo")
```

### 15.1.2 按规则分类整理——自动归档

下载文件夹里混杂了文档、图片、压缩包、安装程序。一条脚本让它们各归其位：

```python
import os
import shutil

# 按扩展名映射到分类文件夹
CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".java", ".cpp", ".go", ".json"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "安装包": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
}

def organize_directory(directory):
    """按文件类型将文件分类到子文件夹中"""
    # 创建分类目录
    for category in CATEGORIES:
        os.makedirs(os.path.join(directory, category), exist_ok=True)

    moved_count = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isdir(filepath):       # 跳过目录
            continue

        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # 找到对应的分类
        for category, extensions in CATEGORIES.items():
            if ext in extensions:
                dest = os.path.join(directory, category, filename)
                shutil.move(filepath, dest)
                print(f"  📁 {category}/ ← {filename}")
                moved_count += 1
                break

    print(f"完成！移动了 {moved_count} 个文件")

# organize_directory("./Downloads")
```

### 15.1.3 批量文件内容操作——搜索与替换

不只是文件名——我们经常需要批量修改文件的内容。比如把项目中的所有 `old_function_name` 替换为 `new_function_name`：

```python
import os
import fnmatch

def find_and_replace(directory, pattern, old_text, new_text, dry_run=True):
    """在匹配 pattern 的文件中查找并替换文本"""
    modified_files = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")]   # 跳过隐藏目录

        for filename in files:
            if not fnmatch.fnmatch(filename, pattern):
                continue

            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue    # 跳过非文本文件

            if old_text not in content:
                continue

            new_content = content.replace(old_text, new_text)

            if dry_run:
                count = content.count(old_text)
                print(f"  🔍 {filepath}: 找到 {count} 处匹配")
                modified_files.append(filepath)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  ✏️ {filepath}: 已替换")

    if dry_run and modified_files:
        print(f"\n预览完成，共 {len(modified_files)} 个文件匹配。去掉 dry_run=True 来正式替换。")

# 预览（安全模式）
# find_and_replace("./project", "*.py", "old_name", "new_name", dry_run=True)
# 正式替换
# find_and_replace("./project", "*.py", "old_name", "new_name", dry_run=False)
```

### 15.1.4 批量备份——带时间戳的快照

```python
import os
import shutil
import zipfile
from datetime import datetime

def backup_directory(source_dir, backup_dir, keep=5):
    """将目录压缩备份，只保留最近 N 个备份"""
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(backup_dir, zip_name)

    # 压缩
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zf.write(file_path, arcname)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ 备份完成: {zip_name} ({size_mb:.1f} MB)")

    # 清理旧备份——只保留最近 keep 个
    backups = sorted(
        [f for f in os.listdir(backup_dir) if f.endswith(".zip")],
        reverse=True
    )
    for old in backups[keep:]:
        os.remove(os.path.join(backup_dir, old))
        print(f"  🗑️ 删除旧备份: {old}")

# backup_directory("./my_project", "./backups", keep=5)
```

### 15.1.5 使用 `pathlib`——面向对象的路径操作

Python 3.4+ 引入了 `pathlib` 模块，提供了一种更现代、更面向对象的文件和目录操作方式。相比 `os.path` 的函数式风格，`pathlib` 的链式调用更加直观：

```python
from pathlib import Path

# 创建 Path 对象
project = Path("./my_project")
data_file = project / "data" / "input.csv"    # 用 / 拼接路径（太优雅了！）

# 检查
print(f"存在: {data_file.exists()}")
print(f"是文件: {data_file.is_file()}")
print(f"后缀: {data_file.suffix}")            # .csv
print(f"文件名: {data_file.stem}")             # input
print(f"父目录: {data_file.parent}")           # my_project/data

# 读写——一行搞定
content = Path("config.json").read_text(encoding="utf-8")
Path("output.txt").write_text("Hello, World!", encoding="utf-8")

# 遍历目录——比 os.listdir() 更强大
# for py_file in Path(".").rglob("*.py"):     # 递归搜索所有 .py 文件
#     print(py_file)

# 批量操作——pathlib 风格的批量重命名
def rename_with_pathlib(directory, old_suffix, new_suffix):
    """将指定后缀的文件全部改为另一个后缀"""
    dir_path = Path(directory)
    for file in dir_path.glob(f"*{old_suffix}"):
        new_name = file.with_suffix(new_suffix)
        file.rename(new_name)
        print(f"  {file.name} → {new_name.name}")
```

### 15.1.6 实战练习

1. 写一个脚本，扫描指定目录下的所有 `.log` 文件，将内容合并为一个文件 `merged.log`，每条日志前面加上来源文件名和时间戳。

2. 编写一个"重复文件查找器"——扫描指定目录，找出内容完全相同的文件（通过比较 MD5 哈希值），按组列出重复文件，并给出释放的空间大小。

3. 使用 `pathlib` 重写 15.1.2 的自动分类整理脚本，将所有 `os` 和 `shutil` 调用替换为 `pathlib` 的等价操作。