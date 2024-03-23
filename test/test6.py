# # 测试符号匹配
# import numpy as np
# import cv2
#
# # 读入图像，截图部分作为模板图片
# img_src = cv2.imread('../tables2/73.png')
# img_templ = cv2.imread('../symbol/0.png')
#
# # 灰度化图像
# gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
# template = cv2.cvtColor(img_templ, cv2.COLOR_BGR2GRAY)
# # 模板匹配
# result_t = cv2.matchTemplate(img_src, img_templ, cv2.TM_CCOEFF_NORMED)
# # 二值化图像
# ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
# # cv2.imshow('1',binary)
# res = cv2.matchTemplate(binary, template, cv2.TM_CCOEFF_NORMED)
#
# # 设置匹配度阈值
# threshold = 0.5
#
# # 使用逻辑表达式筛选匹配度数组中超过阈值的数值
# locations = np.where(res >= threshold)
#
# # 定义保存坐标的列表
# rectangles = []
#
# # 遍历匹配度超过阈值的位置，并在原图上绘制矩形框
# for pt in zip(*locations[::-1]):
#     bottom_right = (pt[0] + template.shape[1], pt[1] + template.shape[0])
#     cv2.rectangle(img_src, pt, bottom_right, (0, 0, 255), 2)
#     rectangles.append((pt, bottom_right))
#
# # 显示结果图像
# cv2.imshow('Matched', img_src)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # 打印保存的坐标信息
# print('Rectangles:', rectangles)

import numpy as np
import cv2

count = 0
for i in range(262):
    img_src = cv2.imread(f'../tables2/{i}.png')
    img_templ = cv2.imread('../symbol/0.png')

    # 灰度化图像
    gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(img_templ, cv2.COLOR_BGR2GRAY)

    # 二值化图像
    ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # cv2.imshow('1',binary)
    res = cv2.matchTemplate(binary, template, cv2.TM_CCOEFF_NORMED)

    # 取匹配程度大于%80的坐标
    threshold = 0.69
    loc = np.where(res >= threshold)

    # 存放匹配符号的区域坐标
    match_box = []
    h, w = img_templ.shape[:2]
    for index, pt in enumerate(zip(*loc[::-1])):
        bottom_right = (pt[0] + w, pt[1] + h)
        # print(bottom_right)
        if index > 0:
            for i, subBox in enumerate(match_box):
                # 排除重复
                if abs(pt[0] - subBox[0][0]) < 10 and abs(bottom_right[0] - subBox[1][0]) < 10 and abs(
                        pt[1] - subBox[0][1]) < 10 and abs(bottom_right[1] - subBox[1][1]) < 10:
                    break
                if i == len(match_box) - 1:
                    match_box.append([pt, bottom_right])
        else:
            match_box.append([pt, bottom_right])
    # 将匹配上的地方用红色方框圈出来
    # for (pt, bottom_right) in match_box:
    #     cv2.rectangle(img_src, pt, bottom_right, (255, 0, 0), 1)

    # 查看匹配的个数是否满足图片的需求
    # print(len(match_box))
    count += len(match_box)

    # cv2.imshow('img_rgb', img_src)
    # cv2.waitKey(0)
print(count)

