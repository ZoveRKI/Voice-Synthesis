import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import questionary

options = {
    "🌟反派": {"album":"反派", "width": 4},
    "🌟七个神兽": {"album":"七个神兽", "width": 3},
    "🌟包围": {"album":"包围", "width": 3},
    "🌟诛仙(旧版)": {"album":"诛仙(旧版)", "width": 3},
    "🌟诛仙(新版)": {"album":"诛仙(新版)", "width": 3},
}

your_choice = questionary.select(
    "Please select a option:",
    choices=[
        f"{key}" for key in options
    ],
    # default="🌟drxsw",        # 默认首选项
    qmark="🌈",
    pointer="👉",
    # use_shortcuts=True,       # 启用键盘快捷键
    # selected_symbol="✔"       # 选中项的符号(多选时使用)
).ask()

FOLDER = './output'
ALBUM = options[your_choice]["album"]
WIDTH = options[your_choice]["width"]

for filename in os.listdir(FOLDER):
    if filename.endswith('.mp3'):
        filepath = os.path.join(FOLDER, filename)
        try:
            audio = EasyID3(filepath)
        except Exception:
            # 文件没有 ID3 标签，先添加一个
            audiofile = MP3(filepath)
            audiofile.add_tags()
            audiofile.save()
            audio = EasyID3(filepath)

        # 修改元数据
        title = os.path.splitext(filename)[0]
        match = re.search(r'\d+', title)

        if not match:
            print(f"文件名 {filename} 中未找到数字，跳过处理。")
            continue

        original_number = match.group()
        padded_number = original_number.zfill(WIDTH)

        if original_number == padded_number:
            new_title = title
        else:
            new_title = re.sub(r'\d+', padded_number, title, count=1)

        audio['title'] = new_title
        audio['album'] = ALBUM
        audio.save()

        new_filename = ALBUM + '-' + new_title + '.mp3'
        new_filepath = os.path.join(FOLDER, new_filename)

        if not os.path.exists(new_filepath):
            os.rename(filepath, new_filepath)
            print(f"✅ 已写入元数据并重命名：{filename} -> {new_filename}")
        else:
            print(f"⚠️ 已跳过：{new_filename} 已存在")
