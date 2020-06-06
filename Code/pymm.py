import requests  # 发起请求所用
from lxml import etree  # xpath语法解析所用
import os  # 操作系统文件所用
import time  # 避免访问频繁，保证睡眠

# 用于爬取爱美女网站指定某章的套图

'''
发起请求：
url
headers -- user-agent 、 referer 、cookie
'''
name = 1

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11",
    'referer': 'https://www.2meinv.com/',
    'cookie': 'p_c_a_hist_1818=A3JWPgJhVzhTdFVgBHUCPg%3D%3D; p_c_a_hist_1617=AXBUPABjWTZQd1VgVSRUaA%3D%3D'
}

siteFont = 'https://www.2meinv.com/article-'
siteBack = '.html'


# 获取网页信息
def get_html(url):
    html = requests.get(url, headers=headers).content.decode('utf-8')
    # print(html)
    return html


# 解析数据
def parse_html(html):
    etree_html = etree.HTML(html)
    # 解析图片链接
    list_img_url = etree_html.xpath('/html/body/div[5]/a/img/@src')
    img_url = list_img_url[0]
    return img_url


# 获取套图的标题作为文件夹名字
def get_package_name(html):
    etree_html = etree.HTML(html)
    # 解析文本标题,此处的【0】是提取返回list中的每一个字符串
    list_text_url = etree_html.xpath('/html/body/div[2]/div/h1/text()')
    # list转str，去除str中的空格以及各种符号
    text = str(list_text_url).replace(' ', '').replace('\'', '').replace('[', '').replace(']', '')
    # print(type(text))
    # print(text)
    return text         # 返回一个str


# 保存图片
def save_img(img_url, text):
    global name
    # 若不存在该文件，则创建一个
    path = "D://Desktop//" + text
    if not os.path.exists(path):
        os.mkdir(path)

    # 相隔6秒爬取
    time.sleep(6)
    # 获取图片，写入文件
    image = requests.get(img_url, headers=headers).content
    print(u'正在下载第%d张图片...' % name)
    with open(path + '/' + '%d.jpg' % name, 'wb') as f:
        f.write(image)
    name += 1


# 输入要爬取的页面的article-值  例如https://www.2meinv.com/article-3117.html就输入3117
def get_article_nums():
    global siteFont, siteBack
    article = str(input("请输入article后的值："))
    return article


# 得到该页面中图片的总数量
def get_img_max(article):
    url = siteFont + article + siteBack
    html1 = requests.get(url, headers=headers).content.decode('utf-8')
    html2 = etree.HTML(html1)
    # nums 是一个列表，然后列表中的每一个值都是一个字典，要转化为int
    nums = int(html2.xpath('/html/body/div[6]/div/a[8]')[0].text)
    # print(type(nums))
    # print(nums)
    return nums


def main():
    global siteFont, siteBack
    article = get_article_nums()
    nums = get_img_max(article)
    for num in range(1, nums + 1):
        url = siteFont + article + '-' + str(num) + siteBack
        html = get_html(url)
        text = get_package_name(html)
        img_url = parse_html(html)
        save_img(img_url, text)


if __name__ == '__main__':
    main()
