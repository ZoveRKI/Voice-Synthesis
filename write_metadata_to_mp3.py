import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB

FOLDER = './output'
ALBUM = str(input("请输入专辑名: "))
WIDTH = int(input("请输入标题的位数: "))

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

        audio['title'] = title
        audio['album'] = ALBUM
        audio.save()

        number = str(match.group()).zfill(WIDTH)
        new_title = re.sub(r'\d+', number, title, count=1)
        new_filename = ALBUM + '-' + new_title + '.mp3'
        new_filepath = os.path.join(FOLDER, new_filename)

        if not os.path.exists(new_filepath):
            os.rename(filepath, new_filepath)
            print(f"✅ 已写入元数据并重命名：{filename} -> {new_filename}")
        else:
            print(f"⚠️ 已跳过：{new_filename} 已存在")
