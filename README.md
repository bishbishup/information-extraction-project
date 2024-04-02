# 表格截取抓取信息项目📈📉

* 打开网址：https://www.futureelectronics.cn/resources/market-conditions-report/batteries?_ga=2.41840161.2004194343.1708663618-1816887471.1708663618网页下方有个大图，其中有多个表格，就是识别表格中的内容

1、从大图识别各个表格的位置然后切割出来

![](./imgs/0.png)

2、对每个表格使用paddleOCR识别厂商、商品的字符串，并对价格趋势的符号进行匹配转换

![](img/1.png)

3、提取出表格所有厂商的有关信息并将结果存储到Result.xlsx中

![](img/2.png)
