# 表格提取
import cv2
import os

# 创建输出文件夹
output_folder1 = 'tables1'
output_folder2 = 'tables2'
if not os.path.exists(output_folder1):
    os.makedirs(output_folder1)
if not os.path.exists(output_folder2):
    os.makedirs(output_folder2)

# pdf转换为图片一共有31张照片
count = 0
for i in range(31):
    # 读取图片
    image = cv2.imread(f'imgs/{i}.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)

    # 轮廓检测
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选并框出需要的表格区域
    for contour in contours:
        # 返回矩形边界左上角顶点的坐标值及矩形边界的宽和高
        x, y, w, h = cv2.boundingRect(contour)
        # area = cv2.contourArea(contour)
        # 通过宽和高的限制来选出符合表格的轮廓
        # h的限制是因为上面有个Logo也会识别到，那部分是无用的信息所以在这里通过h筛选掉
        if w <= 485 and w >= 475 and h >= 60:
            # 整张表丢进去识别的话中间有些无关的信息也会提取到所以分开两部分来处理
            # 将第一列存储到tables1中去
            cropped_image = image[y + 45:y + h, x:x + 236]
            cv2.imwrite(os.path.join(output_folder1, f'{count}.png'), cropped_image)
            # 将价格趋势存储到tables2中去
            cropped_image = image[y + 45:y + h, x + 395:x + w]
            cv2.imwrite(os.path.join(output_folder2, f'{count}.png'), cropped_image)
            count += 1
            # 绘制红色矩形框
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.destroyAllWindows()