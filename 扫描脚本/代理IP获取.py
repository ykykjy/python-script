import urllib.request
import urllib.error
from lxml import etree
import requests
# import ssl  # ssl用于强行使用https协议却又没有证书的网站
#
# ssl._create_default_https_context = ssl._create_unverified_context


def check_proxy(ip, port):
    """
    检查是不是可用IP和端口
    :param ip:  代理IP
    :param port:  代理IP端口
    :return:
    """
    url = 'http://www.baidu.com'  # 通过访问百度来获取代理IP是否正确
    try:
        ip_port = f"{ip}:{port}"
        proxy = {  # 直接在get方法的后面添加proxies参数即可
            'https': ip_port
        }
        response = requests.get(url=url, proxies=proxy)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'channelid=0; sid=1680441715194493; _gcl_au=1.1.1024908624.1680441714; '
                  '_ga=GA1.2.140581713.1680441715; '
                  '_gid=GA1.2.615657752.1680441715; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1680441714,1680484020; '
                  '_gat=1; sessionid=999a8574505d730c6828c39b1f5c6380; '
                  'Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1680484130',
        'Host': 'www.kuaidaili.com',
        'Referer': 'https://www.kuaidaili.com/free/inha/1/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Mobile Safari/537.36',
    }

    try:
        for i in range(2, 10):
            ip = []
            url = f"https://www.kuaidaili.com/free/inha/{i}/"
            requst = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(requst)
            content = response.read().decode('utf-8')

            tree = etree.HTML(content)
            ip_list = tree.xpath("//*[@id='list']/table/tbody/tr/td[1]/text()")
            port_list = tree.xpath("//*[@id='list']/table/tbody/tr/td[2]/text()")
            for item in range(len(ip_list)):
                if check_proxy(ip_list[item], port_list[item]):
                    str = ip_list[item] + ':' + port_list[item]
                    ip.append(str)
            print(ip)
    except urllib.error.URLError as error:
        print(error)
