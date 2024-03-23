# 表格厂商以及商品的字符串识别并写进excel
import cv2
from paddleocr import PaddleOCR
import pandas as pd

# 初始化 PaddleOCR
ocr = PaddleOCR()

# 处理（、*、(的方法(通用)
def merge_list_elements1(lst):
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

tempres = []
res = []
for i in range(262):
    # 我的方法截取的图片右上角有小字符串会被误判识别出来
    if i == 16 or i == 75 or i == 132 or i == 211:
        # 读取图片
        image = cv2.imread(f'tables1/{i}.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)

        # 轮廓检测
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

        # 图像预处理
        img2 = cv2.cvtColor(image[y:y+h,x:x+194], cv2.COLOR_BGR2RGB)

        # 执行 OCR 识别
        result = ocr.ocr(img2)

        # 解析识别结果
        for line in result:
            # print(line)
            for word in line:
                # print(word[-1])
                # print(word[1][0])
                tempres.append(word[1][0])
            res.append(tempres)
            tempres = []
    else:
        # 读取图片
        image = cv2.imread(f'tables1/{i}.png')

        # 图像预处理
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 执行 OCR 识别
        result = ocr.ocr(image)

        # 解析识别结果
        for line in result:
            # print(line)
            for word in line:
                # print(word[-1])
                # print(word[1][0])
                tempres.append(word[1][0])
            # 处理子公司的第一种情况
            if i == 145:
                merged_list = merge_list_elements3(tempres)
            # 处理子公司的第二种情况：
            elif i == 148:
                merged_list = merge_list_elements4(tempres)
            # 处理注释有两行的照片
            elif i == 110 or i == 222:
                merged_list = merge_list_elements2(tempres)
            # 通用方法
            else:
                merged_list = merge_list_elements1(tempres)
            # 特殊图片该厂商有些子厂商在下面不易处理
            res.append(merged_list)
            tempres = []

# print(res)

formatted_data = []
for item in res:
    vendor = item[0]
    products = item[1:]
    if len(products) == 1:
        formatted_data.append([vendor, products[0]])
    else:
        formatted_data.append([vendor, products])

# print(formatted_data)

# 创建一个空的 DataFrame
df = pd.DataFrame(columns=['厂商', '商品'])

# 将原始数据填充到 DataFrame 中
for item in formatted_data:
    vendor = item[0]
    products = item[1]
    if isinstance(products, list):
        for product in products:
            temp_df = pd.DataFrame([[vendor, product]], columns=['厂商', '商品'])
            df = pd.concat([df, temp_df], ignore_index=True)
    else:
        temp_df = pd.DataFrame([[vendor, products]], columns=['厂商', '商品'])
        df = pd.concat([df, temp_df], ignore_index=True)

# 将数据写入 Excel 文件
df.to_excel('Result.xlsx', index=False)
