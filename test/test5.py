# 针对个别logo会被识别到的图片做的去logo测试
import cv2
from paddleocr import PaddleOCR

# 初始化 PaddleOCR
ocr = PaddleOCR()

# 读取图片
image = cv2.imread('../tables1/7.png')

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

# 解析识别结果
for line in result:
    for word in line:
        print(word[1])
        print(word[1][0])

print(result)