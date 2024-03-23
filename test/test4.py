# 测试将data数据写进excel
import pandas as pd

# 定义原始数据
data = [['MaxLinear', '接口'],
        ['Infineon', ['传感器', '开关稳压器', '汽车模拟和电源', '(CAN/LIN/SmartFET)']],
        ['FTDI Chip', '接口'],
        ['Diodes Incorporated', ['多源模拟/电源', '开关稳压器']],
        ['Bosch Sensortec', '传感器'],
        ['ams', '传感器'],
        ['ROHM', ['传感器', '开关稳压器']]]

# 创建一个空的 DataFrame
df = pd.DataFrame(columns=['厂商', '商品'])

# 将原始数据填充到 DataFrame 中
for item in data:
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