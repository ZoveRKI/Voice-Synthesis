import os
import asyncio
import glob
import re
from bs4 import BeautifulSoup
from edge_tts import Communicate

HTML_FOLDER = "html"
OUTPUT_FOLDER = "output"
VOICE = "zh-CN-YunxiNeural"
RATE = "+25%"
MAX_CONCURRENT_TASKS = 32

# 保证输出目录存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_number(filename):
    match = re.search(r"(\d+)", os.path.basename(filename))
    return int(match.group(1)) if match else float('inf')

# 提取 HTML 中的文本
def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(strip=True)

# 异步合成语音
async def synthesize_to_mp3(text, output_path, rate='+0%', semaphore=None):
    async with semaphore:
        communicate = Communicate(text, VOICE, rate=rate)
        await communicate.save(output_path)
        print(f"完成合成: {output_path}")

# 主流程
async def main():
    html_files = glob.glob(os.path.join(HTML_FOLDER, "*.html"))
    html_files.sort(key=extract_number)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    tasks = []
    generated_count = 0
    skipped_files = []

    for file_path in html_files:
        file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.mp3"
        output_path = os.path.join(OUTPUT_FOLDER, file_name)

        if os.path.exists(output_path):
            skipped_files.append(file_name)
            continue
        pass

        text = extract_text_from_html(file_path)
        print(f"正在合成 {file_name} ...")
        task = asyncio.create_task(synthesize_to_mp3(text, output_path, RATE, semaphore))
        tasks.append(task)
        generated_count += 1

    await asyncio.gather(*tasks)
    print(f"✅ 已生成 {generated_count}个MP3文件在目录: {OUTPUT_FOLDER}")
    if skipped_files:
        print(f"❌ 以下文件已存在，未覆盖：{', '.join(skipped_files)}")
    pass

# 执行
if __name__ == "__main__":
    asyncio.run(main())
