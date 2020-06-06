import requests  # 发起请求所用
from lxml import etree  # xpath语法解析所用
import os  # 操作系统文件所用
import time  # 避免访问频繁，保证睡眠

# 用于爬取爱美女网站所有的标签以及对应访问链接

'''
发起请求：
url
headers -- user-agent 、 referer 、cookie等
'''
name = 1
tag = 1
link = 1
num = 1
nums = 387

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11",
    'referer': 'https://www.2meinv.com/tags-all.html',
    'cookie': 'p_c_a_hist_1596=UyIPZwtoAG9RdldiWyoEOA%3D%3D' ' p_c_a_hist_1789=B3ZTOwdkVToCJQYzAHFWag%3D%3D'
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
    global link
    etree_html = etree.HTML(html)
    # 解析tags标题的链接
    '''
    第一行第一个的链接：
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[1]/a/@href
    第一行最后一个：                                ↓↓
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[8]/a/@href
    最后一行最后一个：                              ↓↓ 
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[387]/a/@href
    '''
    # tags = 387
    # for tag in range(1, tags + 1):
    list_links_url = etree_html.xpath('/html/body/div[3]/div/div[1]/div[2]/div/ul/li[' + str(link) + ']/a/@href')
    # list 转 str
    links_url = str(list_links_url).replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
    link += 1
    return links_url
    # print(type(links_url))        # 打印验证是否获取到所需str
    # print(links_url)


# 获取tag的标题作为文件夹名字
def get_package_name(html):
    global tag
    etree_html = etree.HTML(html)
    '''
    目测第一行，有8个tags，标题从
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[1]/a
    到                                            ↓↓
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[8]/a
    变化为最后一个li[1]-[8]
    第二行开始为：同样只是最后一个元素变了             ↓↓
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[9]/a
    最后一行最后一个：                              ↓↓
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[387]/a
    所以，定位到标题：
    /html/body/div[3]/div/div[1]/div[2]/div/ul/li[x]/a[@title]
    '''
    # tags = 387
    # for tag in range(1, tags + 1):
    # 解析文本标题,此处的【0】是提取返回list中的每一个字符串,再转str
    list_title_url = etree_html.xpath(
        '/html/body/div[3]/div/div[1]/div[2]/div/ul/li[' + str(tag) + ']/a[@title]/text()')
    # str类型，去除str中的空格
    title = str(list_title_url).replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
    # print(type(title))
    # print(title)
    tag += 1
    return title  # 返回str


# 保存链接
def save_info(links_url, title):
    global name
    # 若不存在该文件，则创建一个
    path = "D://Desktop//" + title
    if not os.path.exists(path):
        os.mkdir(path)

    # 相隔n秒爬取
    time.sleep(7)
    # 取图片，写入文件
    links_text = links_url
    print(u'正在写入第%d个链接...' % name)
    with open(path + '/' + '%d.txt' % name, 'w', encoding="utf-8") as f:
        f.write(links_text)
    name += 1


def main():
    global num, nums
    for num in range(1, nums + 1):
        url = 'https://www.2meinv.com/tags-all.html'
        html = get_html(url)
        links_url = parse_html(html)
        title = get_package_name(html)
        save_info(links_url, title)


if __name__ == '__main__':
    main()
