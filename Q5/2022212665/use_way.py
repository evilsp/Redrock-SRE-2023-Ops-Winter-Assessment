import pymysql
import time, paramiko

# 添加用户
def add_user(username):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306, charset='utf8')
    cursor = db.cursor()
    # 为每个用户创建自己的表，储存数据
    sql1 = f"create table {username}(num varchar(50) not null ,hostname varchar(30) not null,account varchar(20) not null,password varchar(200) not null,way varchar(20) not null,primary key(num))ENGINE = InnoDB DEFAULT CHARSET = utf8;"
    sql2 = f"create table {username}_configuration(id int not null auto_increment,peizhi varchar(1000) not null,num varchar(20) not null,primary key(id))ENGINE = InnoDB DEFAULT CHARSET = utf8;"
    sql3 = f"create table {username}_key(id int not null auto_increment,sshkey varchar(1000) not null,num varchar(20) not null,primary key(id))ENGINE = InnoDB DEFAULT CHARSET = utf8;"
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        db.commit()
        return '添加成功！'
    except Exception as e:
        db.rollback()
        return '登入成功！'
    finally:
        db.close()

# 添加主机信息
def add_hostname(username, num, hostname, account, password, way):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = f"insert into {username} (num,hostname,account,password,way) values ('{num}','{hostname}','{account}','{password}','{way}');"
    try:
        cursor.execute(sql)
        db.commit()
        return '添加成功！'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 添加密钥
def add_key(username, num, key):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = f"insert into {username}_key (sshkey,num) values ('{key}','{num}');"
    try:
        cursor.execute(sql)
        db.commit()
        return '添加成功！'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 获取密钥
def get_key(username, num):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()

    sql = f'select sshkey from {username}_key where num={num};'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        num = len(result)
        if num == 0:
            return '此主机还没有配置'
        else:
            return f'{result}'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 查看所有主机
def view_datd(username):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()
    sql = f'select count(*) from {username};'
    sql1 = f'select num,hostname,account,way from {username};'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        num = result[0][0]
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        x = [num, result1]
        return x
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()


# 删除主机信息
def del_data(username, num):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')
    cursor = db.cursor()
    sql = f"delete from {username} where num = '{num}';"
    sql1 = f"delete from {username}_configuration where num = '{num}';"
    try:
        cursor.execute(sql)
        cursor.execute(sql1)
        db.commit()
        return '删除成功'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()


# 查看某个主机的配置
def view_configuration(username, i):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()

    sql = f'select id,peizhi from {username}_configuration where num="{i}";'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        num = int(len(result))
        if num == 0:
            return '此主机还没有配置'
        else:
            return f'此主机的配置为：{result}'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 更改某个主机的配置
def change_configuration(username, change_id, change_peizhi):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()
    sql = f'update {username}_configuration set peizhi=\'{change_peizhi}\' where id={change_id};'
    try:
        cursor.execute(sql)
        db.commit()
        return '修改成功!'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 删除某个主机的配置
def del_configuration(username, num):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()

    sql = f'delete from {username}_configuration where id="{num}";'
    try:
        cursor.execute(sql)
        db.commit()
        return '删除成功！'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 增加某个主机的配置
def add_configuration(username, add_peizhi, num):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()
    db.commit()
    sql = f'insert into {username}_configuration values(null,\'{add_peizhi}\',"{num}");'
    try:
        cursor.execute(sql)
        db.commit()
        return '添加成功！'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 获取某个主机的信息
def get_message(username, i):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()

    sql = f'select *from {username} where num={i};'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0]
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()

# 获取某个主机的配置
def get_configuration(username, i):
    db = pymysql.connect(host="47.109.56.167", user="root", password="zzlniu", db="ssh_link", port=3306,
                         charset='utf8')

    cursor = db.cursor()

    sql = f'select peizhi from {username}_configuration where num="{i}";'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        num = len(result)
        if num == 0:
            return '此主机还没有配置'
        else:
            return f'{result}'
    except Exception as e:
        db.rollback()  # 如果出错就回滚并且抛出错误收集错误信息。
        return "Error!:{0}".format(e)
    finally:
        db.close()


