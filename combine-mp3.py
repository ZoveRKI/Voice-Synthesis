import os
import re
import sys
from moviepy import AudioFileClip, concatenate_audioclips

# 设置你的 MP3 文件目录
PATH = "./output"

# 获取所有 mp3 文件并排序
mp3_files = sorted([
    f for f in os.listdir(PATH)
    if f.lower().endswith(".mp3")
])

if not mp3_files:
    print("❌ 未找到任何 MP3 文件，程序已终止。")
    sys.exit(1)

match = re.search(r'\d+', mp3_files[0])
output_file = match.group() + '.mp3'

print("待合成Mp3文件列表：" + str(mp3_files))
print("输出文件名：" + output_file)

clips = [AudioFileClip(os.path.join(PATH, f)) for f in mp3_files]

final_clip = concatenate_audioclips(clips)
final_clip.write_audiofile(
    os.path.join(PATH, output_file),
    bitrate="48k",
    ffmpeg_params=["-ac", "1", "-ar", "24000"],
)
