import re
import requests

url = "http://192.168.93.129/1.php"

content = requests.get(url=url)
content = content.text  # 获取网页源码
ret = re.match("flag.+}", content)
fp = open('flag.txt', 'a')
fp.write(ret.group())
fp.close()
