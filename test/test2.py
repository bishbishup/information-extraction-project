# 第一天截取的表格
import cv2
import os
import numpy as np

# 读取图片
image = cv2.imread('../imgs/0.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化处理
_, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)

# 轮廓检测
contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # 在空白画布上绘制轮廓
# contour_img = np.zeros_like(image)
# cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
#
# # 在原始图像上绘制轮廓
# contour_image = image.copy()
# cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
#
# # 显示绘制轮廓后的图片
# cv2.imshow('Contours on Blank Image', contour_img)
# cv2.imshow('Contours on Original Image', contour_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 筛选并框出需要的表格区域
count = 0
output_folder = 'temp'
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    if w <= 476 and w >= 475:
        # 观察得知根据宽度来判断比较合适
        print(w)
        print(h)
        # 去LOGO
        cropped_image = image[y+60:y + h, x:x + w]
        cv2.imwrite(os.path.join(output_folder, f'{count}.png'), cropped_image)
        count += 1
        # 绘制红色矩形框
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 显示标记表格后的图片
cv2.imshow('Tables Highlighted', image)
cv2.waitKey(0)
cv2.destroyAllWindows()