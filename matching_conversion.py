# 符号匹配转换成文字
import numpy as np
import cv2
import pandas as pd

final = []
for i in range(262):
    img_src = cv2.imread(f'tables2/{i}.png')
    result = []
    for j in range(5):
        if j == 0:
            tag = "稳定"
        elif j == 1:
            tag = '延长/上涨'
        elif j == 2:
            tag = '缩短/下降'
        elif j == 3:
            tag = '依据市场进行选择性调整'
        elif j == 4:
            tag = '未知'
        img_templ = cv2.imread(f'symbol/{j}.png')

        # 灰度化图像
        gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(img_templ, cv2.COLOR_BGR2GRAY)
        # 二值化图像
        ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # 进行匹配
        res = cv2.matchTemplate(binary, template, cv2.TM_CCOEFF_NORMED)

        # 经过多次测试最终取匹配程度大于百分之69的坐标
        threshold = 0.69
        # 提取大于0.69的结果
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
                        match_box.append([pt, bottom_right,tag])
            else:
                match_box.append([pt, bottom_right,tag])
        result = result + match_box
        # 将匹配上的地方用红色方框圈出来
        # for (pt,bottom_right,tag) in match_box:
        #      cv2.rectangle(img_src, pt, bottom_right, (255, 0, 0), 1)
        # cv2.imshow('img_rgb', img_src)
        # cv2.waitKey(0)

        # 查看匹配的个数是否满足图片的需求
        # print(len(match_box))
        # print(match_box)
    # 按照矩形区域的第一个元组中纵坐标的起始值进行排序
    sorted_rectangles = sorted(result, key=lambda x: x[0][1])
    # 提取文字部分组成临时数组
    temp_labels = []
    temp_labels = [rectangle[2] for rectangle in sorted_rectangles]
    final.append(temp_labels)

# 读取之前以及存放好的文件
df1 = pd.read_excel('Result.xlsx')

# 转换成能插入进excel表格的东西
flat_list = [item for sublist in final for item in sublist]

# 将价格趋势另起一个表再插入上述表格(由于左边关于厂商和商品的还没处理完全所以不能直接插入第三列，要分成两个表格合并)
df2 = pd.DataFrame(flat_list, columns=['价格趋势'])

# 连接两个 DataFrame
df = pd.concat([df1, df2], axis=1)

# 将更新后的 DataFrame 写入到同一文件
df.to_excel('Result.xlsx', index=False)
