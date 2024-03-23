# 处理（、*、(的方法
def merge_list_elements(lst):
    merged_lst = []
    current_text = ""

    for text in lst:
        if merged_lst and (text.startswith("(") or text.startswith("*") or text.startswith("（")):
            merged_lst[-1] += text
        elif "、" in text:
            current_text += text
        else:
            if current_text:
                merged_lst.append(current_text)
                current_text = ""
            merged_lst.append(text)

    if current_text:
        merged_lst.append(current_text)

    return merged_lst

# 处理注释有两行的照片
def merge_list_elements2(lst):
    merged_lst = []

    for text in lst:
        merge_flag =  text.startswith("除") or text.startswith("系") or text.startswith('意')
        if merged_lst and merge_flag:
            merged_lst[-1] += text
        else:
            merged_lst.append(text)

    return merged_lst

# 处理子公司的第一种情况
def merge_list_elements3(lst):
    merged_lst = []

    for text in lst:
        merge_flag = "32位MCU" in text or text.startswith("F") or text.startswith("M")
        if merged_lst and merge_flag:
            merged_lst[-1] += text
        else:
            merged_lst.append(text)

    return merged_lst

# 处理子公司的第二种情况
def merge_list_elements4(lst):
    if len(lst) >= 2:
        lst[-2] += lst[-1]
        lst.pop()
    return lst

# 示例用法
text_list = ['STMicroelectronics', '8位MCU', '汽车', '32位MPU', 'STMicroelectronics-STM32', '32位MCU', 'STMicroelectronics-STM32', '32位MCU', 'STMicroelectronics-STM32', '32位MCU', 'STMicroelectronics-其他32', 'MCU', '32位MCU', 'STMicroelectronics-STM32', 'F4/F7/H7', '32位MCU']
merged_list = merge_list_elements3(text_list)
print(merged_list)