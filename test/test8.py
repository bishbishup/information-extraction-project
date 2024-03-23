import cv2
from paddleocr import PaddleOCR

# 初始化 PaddleOCR
ocr = PaddleOCR()

# 处理（、*、(以及、的方法
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
        merge_flag = "32位MCU" in text
        if merged_lst and merge_flag:
            merged_lst[-1] += text
        else:
            merged_lst.append(text)

    return merged_lst

# 读取图片
image = cv2.imread('../tables1/132.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化处理
_, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)

# 轮廓检测
contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
     x, y, w, h = cv2.boundingRect(contour)

# 图像预处理
img = cv2.cvtColor(image[y:y+h,x:x+194], cv2.COLOR_BGR2RGB)

# 执行 OCR 识别
result = ocr.ocr(img)

tempres = []
# 解析识别结果
for line in result:
   # print(line)
   for word in line:
      # print(word[-1])
      print(word[1][0])
      tempres.append(word[1][0])
   merged_list = merge_list_elements2(tempres)

print(merged_list)
