#! /usr/bin/python
# -*- coding: utf8 -*-
import pymysql
import time


class Mydb(object):
    def __init__(self, ip):
        self.ip = ip

    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def connect(self):
        try:
            self.db = pymysql.connect(
                # host='127.0.0.1',
                host=self.ip,
                # port='3306',
                user='guest',
                passwd='guest',
                db='pay_cost'
            )
            self.cursor = self.db.cursor()

        except:
            return False
        else:
            return True

    # 执行更改,insert使用
    def excute(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        # 获取返回的信息
        data = self.cursor.fetchone()
        print(data)

    # 余额查询,返回余额float
    def select_max(self):
        sql = 'select balance from mycost where id=(select max(id) from mycost)'
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # data = float(data[0])
        # print(data[0])
        # print(type(str(data[0])))
        # print(float(data[0]))
        # print(type(float(data[0])))
        return float(data[0])

    # 查询函数
    def select_sql(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    # 用时间和备注查询数据库文件
    def select_db(self, first_time, last_time, infor=''):
        first_time = first_time + ' 00:00:00'
        last_time = last_time + ' 23:59:59'
        # sql = 'select * from mycost where cost_time between "' + first_time + '" and "' + last_time + '"'
        # sql = sql + ' and information like "%' + infor + '%"'
        sql = "select * from mycost where cost_time between '%s' and '%s' and information like '%%%s%%'" %(first_time, last_time, infor)
        try:
            self.cursor.execute(sql)
            reslist = self.cursor.fetchall()
            print(reslist)
            print(type(reslist[0][1]))
            print(reslist[0][1])
            print(len(reslist))
            return reslist
            # for row in reslist:
            #     print('%d--%d' % (row[0], row[1]))
        except:
            # 如果提交失败，回滚到上一次数据
            self.db.rollback()
            return None

    # 修改余额文件
    def fix_balan(self, balance):
        sql = 'insert into mycost(cost_time, cost, balance, information) '
        sql = sql + 'values("' + time.strftime('%Y-%m-%d %H:%M:%S') + '", 0, ' + balance + ', "余额更正")'
        self.cursor.execute(sql)
        self.db.commit()
        # 获取返回的信息
        data = self.cursor.fetchone()
        print(data)

    # 关闭连接
    def close(self):
        # 断开连接
        try:
            self.cursor.close()
            self.db.close()
        except AttributeError:
            print('关闭数据库失败')


if __name__ == '__main__':
    db = Mydb('127.0.0.1')
    db.connect()
    # db.excute("insert into mycost(cost_time, cost, balance, information) values('2019-08-20 22:10:00',50,1000,'测试2')")
    # time.sleep(3)
    # db.select_db('2019-08-20', '2019-08-20', '上')
    # db.select_max()
    # db.fix_balan('1000')
    db.close()
