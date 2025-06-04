import os

def generate_html_files(start, end, output_dir):
    if not output_dir:
        output_dir = "."
    pass

    os.makedirs(output_dir, exist_ok=True)
    generated_count = 0
    skipped_files = []

    for i in range(start, end + 1):
        filename = f"{i}.html"
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            skipped_files.append(filename)
            continue
        pass

        html_content = f"<!-- {i} -->\n<p>\n</p>"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        pass
        generated_count += 1
    pass

    print(f"✨ 生成区间{start}~{end}")
    print(f"✅ 已生成 {generated_count}个HTML文件在目录: {output_dir}")
    if skipped_files:
        print(f"❌ 以下文件已存在，未覆盖：{', '.join(skipped_files)}")
    pass
pass

if __name__ == "__main__":
    try:
        start = int(input("请输入起始数字: "))
        end = int(input("请输入结束数字: "))
        output_dir = str(input("请输入输出目录(默认当前目录): ")).strip()

        if start > end:
            print("❌ 结束数字必须大于起始数字")
        else:
            generate_html_files(start, end, output_dir)
    except ValueError:
        print("❌ 请输入一个有效的整数")
    pass
pass
