import _thread
import time
from subprocess import Popen, PIPE


def ping_check(ip):
    check = Popen("ping {0} \n".format(ip), stdin=PIPE, stdout=PIPE, shell=True)  # 在shell环境下输入ping IP
    data = check.stdout.read()  # 读取shell中输出的数据
    data = data.decode("gbk")  # 编码转换:byte->str
    fp = open('ip.txt', 'a')
    if 'TTL' in data:  # 如果ping成功，就有TTL值
        fp.write(ip)
    fp.close()


# 主函数
if __name__ == '__main__':
    for i in range(1, 255):
        ip = '192.168.93.' + str(i)
        _thread.start_new_thread(ping_check, (ip,))
        time.sleep(0.1)
