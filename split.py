import re
import os

output_dir = str(input("请输入输出目录（默认当前目录）：")).strip()

if not output_dir:
    output_dir = "."

os.makedirs(output_dir, exist_ok=True)

with open("temp.html", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'(<!--\s*(\d+)\s*-->\s*<p>.*?</p>)'
matches = re.finditer(pattern, content, re.DOTALL)

for match in matches:
    full_block = match.group(1)
    id_ = match.group(2)
    filename = os.path.join(output_dir, f"{id_}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_block.strip())
    print(f"Written: {filename}")
