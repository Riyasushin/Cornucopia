import requests
from bs4 import BeautifulSoup
import os

# 目标网站的URL
url = "https://eecs189.org/resources.html"  # 这里替换成你实际要爬取的网站地址
name='cs189'
# 发送GET请求获取网页内容
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 创建一个文件夹用于存放下载的PDF文件
if not os.path.exists(name):
    os.makedirs(name)

# 遍历页面中所有的链接
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith('.pdf'):
        # 处理相对链接转成绝对链接（如果有需要，根据实际网站情况调整）
        if href.startswith('/'):
            # 去除href开头的/，再和目标网址的根路径部分拼接
            # full_url = url.rstrip('/') + href.lstrip('/')
            full_url = 'https://eecs189.org' + href
            # print(full_url)
            # print(href)
            # exit(0)
        else:
            full_url = href

        try:
            # 发送请求获取PDF文件内容
            pdf_response = requests.get(full_url, stream=True)
            if pdf_response.status_code == 200:
                # 获取文件名（从链接中截取最后一段作为文件名）
                file_name = os.path.join(name, href.split('/')[-1])
                with open(file_name, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"已成功下载: {file_name}")
            else:
                print(f"下载 {full_url} 出现问题，状态码: {pdf_response.status_code}")
        except requests.RequestException as e:
            print(f"下载 {full_url} 时出错: {str(e)}")