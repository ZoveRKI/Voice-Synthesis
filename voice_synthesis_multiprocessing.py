import os
import glob
import re
from bs4 import BeautifulSoup
from edge_tts import Communicate
import multiprocessing
import asyncio

HTML_FOLDER = "html"
OUTPUT_FOLDER = "output"
VOICE = "zh-CN-YunxiNeural"
RATE = "+25%"
NUM_PROCESSES = os.cpu_count() or 4  # 根据CPU核心数自动设置并行数

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_number(filename):
    match = re.search(r"(\d+)", os.path.basename(filename))
    return int(match.group(1)) if match else float('inf')

def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(strip=True)

def worker(file_path):
    file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.mp3"
    output_path = os.path.join(OUTPUT_FOLDER, file_name)

    if os.path.exists(output_path):
        return {"skip": file_name}

    text = extract_text_from_html(file_path)

    async def run_tts():
        communicate = Communicate(text, VOICE, rate=RATE)
        await communicate.save(output_path)

    try:
        asyncio.run(run_tts())
        print(f"完成合成: {output_path}")
        return {"done": file_name}
    except Exception as e:
        print(f"*合成失败: {file_name}, 错误: {e}")
        return {"error": file_name, "reason": str(e)}

def main():
    html_files = glob.glob(os.path.join(HTML_FOLDER, "*.html"))
    html_files.sort(key=extract_number)
    generated_count = 0
    skipped_files = []
    failed_files = []

    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        for r in pool.imap_unordered(worker, html_files):
            if r.get("done"):
                generated_count += 1
            elif r.get("skip"):
                skipped_files.append(r["skip"])
            elif r.get("error"):
                failed_files.append(f"{r['error']} ({r['reason']})")

    print(f"✅ 已生成 {generated_count} 个 HTML 文件在目录: {OUTPUT_FOLDER}")
    if skipped_files:
        print(f"✨ 以下总计{len(skipped_files)}个文件已存在，未覆盖：{', '.join(skipped_files)}")
    if failed_files:
        print(f"❌ 以下 {len(failed_files)} 个文件合成失败：")
        for fail in failed_files:
            print(f"   - {fail}")

# 如果你在 Windows 上运行，请确保使用 if __name__ == "__main__": 包裹主逻辑，否则会报错。
if __name__ == "__main__":
    main()
