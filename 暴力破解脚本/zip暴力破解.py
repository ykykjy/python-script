import zipfile
import itertools  # 导入所需模块

filename = "1.zip"  # 待解压文件名


def uncompress(file, passwd):
    """
    定义函数,传入密码对文件进行解压
    :param file: 文件名称
    :param passwd: 要破解文件加密的密码
    :return: 破解成功返回true，失败返回false
    """
    try:
        with zipfile.ZipFile(file) as zf:
            # ./表示当前文件夹，密码选择utf-8编码
            zf.extractall("./", pwd=passwd.encode("utf-8"))
        return True
    except:
        return False


# 生成候选集a-z，0-9,使用全排列的形式生成密码字典
chars = "abcdefghijklmnopqrstuvwxyz0123456789"  # chars为密码可能的字符
for c in itertools.permutations(chars, 4):  # 4代表密码的位数
    password = "".join(c)
    print(password)
    result = uncompress(filename, password)
    if not result:
        print("解压失败", password)
    else:
        print("解压成功", password)
        break
