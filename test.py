import requests
from lxml import etree


url = 'http://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E7%BE%8E%E7%9A%84%E9%9B%86%E5%9B%A2&medium=1'
# 加入UA伪装
headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
           
           }

res = requests.get(url,headers=headers)
print(res.status_code)
print(len(res.text))
html_tree = etree.HTML(res.text)
# 获取所有标题
titles = html_tree.xpath('//a[@class="news-title-font_1xS-F"]/@aria-label')
print(titles)
# 获取所有链接
links = html_tree.xpath('//a[@class="news-title-font_1xS-F"]/@href')
print(links)
