# 合并一些多行的文本
def merge_lines(text_lines):
    merged_text = ""

    # 用于记录上一行文本是否需要合并
    merge_flag = False

    for line in text_lines:
        line = line.strip()  # 去除前后空格
        if merge_flag:
            merged_text = merged_text + line
        else:
            merged_text = merged_text + " " + line

        # 判断下一行是否需要合并
        merge_flag = line.startswith("(") or line.startswith("*")

    return merged_text

# 示例用法
text_lines = [
    "这是一行文本",
    "这是另一行文本",
    "(这是需要合并的下一行文本",
    "*这是需要合并的下一行文本继续",
    "这是另一句话的第一行",
    "这是另一句话的第二行"
]

merged_text = merge_lines(text_lines)
print(merged_text)