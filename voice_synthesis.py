import os
import asyncio
import glob
from bs4 import BeautifulSoup
from edge_tts import Communicate

HTML_FOLDER = "html"
OUTPUT_FOLDER = "output"
VOICE = "zh-CN-YunxiNeural"
RATE = "+25%"

# 保证输出目录存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 提取 HTML 中的文本
def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(strip=True)

# 异步合成语音
async def synthesize_to_mp3(text, output_path, rate='+0%'):
    communicate = Communicate(text, VOICE, rate=rate)
    await communicate.save(output_path)

# 主流程
async def main():
    html_files = glob.glob(os.path.join(HTML_FOLDER, "*.html"))
    for file_path in html_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_name}.mp3")
        text = extract_text_from_html(file_path)
        print(f"正在合成 {file_name}.mp3 ...")
        await synthesize_to_mp3(text, output_path, RATE)

# 执行
if __name__ == "__main__":
    asyncio.run(main())
