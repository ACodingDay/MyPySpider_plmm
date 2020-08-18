import requests  # 发起请求所用
from lxml import etree  # xpath语法解析所用
import os  # 操作系统文件所用
import time  # 避免访问频繁，保证睡眠
from collections import Counter  # 统计list中某一元素的个数

# 用于爬取爱美女网站某一个的标签下的全部套图（分页）

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0 "
                  "AppleWebKit/537.36(KHTML, like Gecko) "
                  "Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11",
    'referer': 'https://www.2meinv.com/',
    'cookie': 'p_c_a_hist_2611=CntVPQRnUj0FIgI3B3ZWag%3D%3D' ' p_c_a_hist_2876=C3gLMlMyBzYHJ188BnJTPQ%3D%3D'
}

# 免费代理IP（百度找）,生成代理IP池
'''
如果你爬的是http://xxx.com这种，那么proxies就http有效;
如果你爬的为https://www.xxx.com这类,那么proxies里面的https内容有效.
'''
proxy_list = [
    '代理ip'
]

# 随机从ip池中选出一个ip
proxy = random.choice(proxy_list)

# 打印出随机选择的代理ip
print("代理IP：" + proxy)

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

siteFont = 'https://www.2meinv.com/tags-'
siteBack = '.html'

name = 1
tag = 1
link = 1
link1 = 1
link2 = 1
num = 1
img_num = 0
img_name = 1
img_nums = 1         # 每一套图的图片数量
link_count = 20  # 一页最多有20套


# 获取网页信息
def get_html(url):
    try:
        html = requests.get(url, headers=headers).content.decode('utf-8')
        # print(html)
        return html
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


# 输入要爬取的页面的标签  例如https://www.2meinv.com/tags-大胸女神.html就输入大胸女神
def get_article_tag():
    atag = str(input("请输入tags后的值(中文)："))
    return atag


# 解析该标签页下的页面数
def parse_pages_html(html):
    etree_html = etree.HTML(html)
    # 解析页数链接
    '''
    观察多页可知有的是：/html/body/div[3]/div/div[2]/div/a[6]；
    有的是 /html/body/div[3]/div/div[2]/div/a[4]；/html/body/div[3]/div/div[2]/div/a[3] ......
    因为最大页数不一样，变的是最后一个数字，无法写死，所以需要根据’下一页‘标签定位到 最后一页
    '''
    list_pages_url = etree_html.xpath('/html/body/div[3]/div/div[2]/div/a[last()-1]')[0].text
    # 需要返回的数值为int型，str 转 int
    pages_num = int(list_pages_url)
    # print(type(pages_num))
    # print(pages_num)
    print(u'---该标签页下有 ' + list_pages_url + u' 页---')
    # print(u'---需要则输入yes，不需要则输入no---')
    return pages_num


# 指定跳转到某一页的数值
def skip_page(pages_num):

    if 'yes' == str(input("请输入yes或者no：")):
        skip_num = int(input("请输入跳转页面的值(数字)："))
        while 1:
            if pages_num >= skip_num >= 1:
                print(u'跳转到第' + str(skip_num) + u'页...')
                return skip_num
            else:
                # 需要重新输入正确的数据
                print(u'输入数据有误！！！请重新输入：')
    else:
        return 0


# 获取跳转页面的信息
def get_skip_html(atag, skip_num):
    global siteFont, siteBack, num
    if skip_num > 0:
        # 跳转的网页url  例如https://www.2meinv.com/tags-xxx-11.html
        skip_url = siteFont + atag + '-' + str(skip_num) + siteBack
        html = requests.get(skip_url, headers=headers).content.decode('utf-8')
        etree_html = etree.HTML(html)
        return etree_html
    else:
        # 不跳转，依然在第一页
        no_skip_url = siteFont + atag + '-' + str(num) + siteBack
        no_skip_html = requests.get(no_skip_url, headers=headers).content.decode('utf-8')
        etree_html = etree.HTML(no_skip_html)
        return etree_html


# 获取跳转/不跳转页面的图片的全部链接
def get_links(etree_html):
    global link1
    # while link_count >= 1:
    # 套图的链接 例如 /html/body/div[3]/div/div[1]/div[2]/ul/li[3]/div/a/@href
    #               /html/body/div[3]/div/div[1]/div[2]/ul/li[1]/div/a
    list_links_url = etree_html.xpath(
            '/html/body/div[3]/div/div[1]/div[2]/ul/li[' + str(link1) + ']/div/a/@href')
    # list 转 str
    links_url = str(list_links_url).replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
    # print(type(links_url))
    # print(links_url)
    # 不为空
    try:
        if links_url is not None:
            # while 循环中直接 return 会导致循环中断！！！直接退出 def 语句块！！！
            return links_url
        else:
            return 'NULL'
    finally:
        link1 += 1       # 一定执行


# 获取跳转/不跳转页面的图片的全部标题
def get_titles(etree_html):
    global link2
    # while link_count >= 1:
    # 套图的标题 例如 /html/body/div[3]/div/div[1]/div[2]/ul/li[1]/div/a
    list_titles_url = etree_html.xpath(
        '/html/body/div[3]/div/div[1]/div[2]/ul/li[' + str(link2) + ']/div/a/text()')
    # list 转 str
    titles_url = str(list_titles_url).replace(' ', '').replace('[', '').replace(']', '').replace('\'', '')
    # print(type(titles_url))        # 打印验证是否获取到所需str
    # print(titles_url)
    try:
        if titles_url is not None:
            return titles_url
        else:
            return 'NULL'
    finally:
        link2 += 1


# 获取链接下的图片
def parse_img_html(links_url):
    html = requests.get(links_url, headers=headers).content.decode('utf-8')
    etree_html = etree.HTML(html)
    # 解析图片链接
    list_img_url = etree_html.xpath('/html/body/div[5]/a/img/@src')
    img_url = list_img_url[0]
    # print(type(img_url))
    # print(img_url)
    return img_url


# 得到该页面中图片的总数量
def get_img_max(links_url):
    global img_nums
    html1 = requests.get(links_url, headers=headers).content.decode('utf-8')
    html2 = etree.HTML(html1)
    # nums 是一个列表，然后列表中的每一个值都是一个字典，要转化为int
    img_nums = int(html2.xpath('/html/body/div[6]/div/a[8]')[0].text)
    # print(type(img_nums))
    # print(img_nums)
    return img_nums


# 保存链接、标题文件
def save_info(atag, titles_url, links_url):
    global name
    titles_text = titles_url
    links_text = links_url
    # 若不存在该tag文件，则创建一个
    path = "Y://PythonGirls//" + atag + "/" + titles_text
    if not os.path.exists(path):
        os.mkdir(path)
        # 相隔n秒爬取
        time.sleep(8)
        # 链接写入文件
        with open(path + '/' + '%d.txt' % name, 'w', encoding="utf-8") as f:
            f.write(links_text)

        print(u'第%d个文件夹创建完成...' % name)
        name += 1
        return path
    else:
        # print(path)
        return path


def save_img(path, img_url):
    global img_name
    # 相隔n秒爬取
    time.sleep(8)
    # 获取图片，写入文件
    image = requests.get(img_url, headers=headers).content
    print(u'第%d张图片下载完成...' % img_name)
    with open(path + '/' + '%d.jpg' % img_name, 'wb') as fb:
        fb.write(image)

    img_name += 1


# 向str字符串插入元素
def str_to_list(str1, anum):
    str2 = '-' + str(anum)
    # str 转 list
    str_list = list(str1)
    str_list.insert(35, str2)
    str1_2 = ''.join(str_list)
    return str1_2
    # print(str1_2)
    # print(type(str1_2))       # 返回str


def main():
    global siteFont, siteBack, num, link_count, img_num, link

    atag = get_article_tag()
    url = siteFont + atag + siteBack
    print(u'访问链接：' + str(url))        # 测试URL正确
    html = get_html(url)
    pages_num = parse_pages_html(html)
    # skip_num = skip_page(pages_num)       # 不跳转，顺序读写
    # 该标签下的页数
    for num in range(1, pages_num + 1):
        etree_html = get_skip_html(atag, skip_num=0)
        # 每页最多20套
        for link in range(1, link_count + 1):
            titles_url = get_titles(etree_html)
            links_url = get_links(etree_html)
            # print(u'第' + str(link) + u'个套图链接：')     # 测试有bug，link数值不是从1开始，而且比正常数值大1
            # print(links_url)            # 经过排查，是全部变量link导致的，为了不混淆，在link后加上数字区分
            # 每一套图的图片总数
            img_max_nums = get_img_max(links_url)
            path = save_info(atag, titles_url, links_url)
            # 保存每一套的图片
            # print(links_url)
            for img_num in range(1, img_max_nums + 1):
                # 保存标题、链接
                links_url1 = str_to_list(links_url, img_num)
                # print(links_url1)
                img_url = parse_img_html(links_url1)
                save_img(path, img_url)
    print("下载完成啦！！！退出程序...")
    sys.exit(0)


if __name__ == '__main__':
    main()
