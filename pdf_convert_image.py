# pdf转图片
import os
import fitz

def pyMuPDF_fitz(pdfPath, imagePath):
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        # 以下两个参数可以调整，分辨率与数值呈正相关
        # 过低的话导致清晰度不足，后续文字识别也识别不到所以需要修改
        # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_x = 2
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix._writeIMG(imagePath + '/' + '%s.png' % pg, 'png', 150)  # 将图片写入指定的文件夹内


if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = 'Market-Conditions-Report-Q4-December-2023-CN.pdf'
    # 2、需要储存图片的目录
    imagePath = './imgs'
    pyMuPDF_fitz(pdfPath, imagePath)



