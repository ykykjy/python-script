import time
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'COUNTRY=NA%2C13.251.126.229; LAST_NEWS=1680526365',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'  # 百度搜索引擎就可以绕过安全狗
}

for paths in open('dict.txt', encoding='utf-8'):  # dict.txt为字典目录
    url = "https://www.php.net"  # 要扫描的URL地址
    paths = paths.replace('\n', '')  # 把末尾的换行去掉
    urls = url + paths
    print(urls)
    proxy = {
        'https': 'z101.kdltps.com:15818'
    }  # 代理池绕过  绕过宝塔
    try:
        code = requests.get(urls, headers=headers, proxies=proxy).status_code
        # time.sleep(3)  # 延迟绕过 ，可以绕过安全狗，宝塔，阿里云
        print(urls + '|' + str(code))
    except Exception as err:
        print(err)