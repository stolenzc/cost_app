from Mysqldb import Mydb
import time
import re


class my_function(object):
    def __init__(self, top_information, cost_time, cost_num, bala_entry, remarks, first_time, last_time, select_infor, tree):
        self.top_information = top_information
        self.cost_time = cost_time
        self.cost_num = cost_num
        self.bala_entry = bala_entry
        self.remarks = remarks
        self.first_time = first_time
        self.last_time = last_time
        self.select_infor = select_infor
        self.tree = tree

    # 屏幕初始化
    def init(self, db):
        self.db = db
        if db.connect():
            self.top_information['text'] = '连接成功,开始记录吧'
        else:
            self.top_information['text'] = '连接失败,请检查你的网络连接和数据库状态'
        self.cost_time.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        # try:
        #     self.bala_entry['text'] = db.select_max()
        # except:
        self.bala_entry['text'] = ' '
        self.first_time.set(time.strftime('%Y-%m-%d'))
        self.last_time.set(time.strftime('%Y-%m-%d'))
        self.cost_num.set('')
        self.remarks.set('')
        self.select_infor.set('')

    # 记录提交
    def commit_fix(self):
        data = self.db.select_sql('select * from mycost where id=(select max(id) from mycost)')
        if str(data[1]) == self.cost_time.get() and (float(data[2]) - float(self.cost_num.get()) < 0.01) and data[4] == self.remarks.get() :
            self.top_information['text'] = '提交失败,请勿重复提交'
        else:
            try:
                balance = self.db.select_max() - float(self.cost_num.get())
                sql = "insert into mycost(cost_time, cost, balance, information) values('%s', '%s', '%s', '%s')" % (self.cost_time.get(), self.cost_num.get(), str(balance), self.remarks.get())
                self.db.excute(sql)
                if self.db.select_max() - balance < 0.01:
                    self.top_information['text'] = '提交成功'
                    self.bala_entry['text'] = balance
                else:
                    self.top_information['text'] = '提交失败'
            except:
                self.top_information['text'] = '提交失败'

    # 查询显示
    def select_and_play(self):
        reslist = self.db.select_db(self.first_time.get(), self.last_time.get(), self.select_infor.get())
        count = 0
        if reslist == None:
            self.top_information['text'] = '查询失败,时间逻辑错误、网络故障或查询结果为零'
        else:
            self.top_information['text'] = '查询成功'
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)
            for i in range(len(reslist)):
                self.tree.insert('', i, text='line' + str(i + 1), value=(str(i + 1), str(reslist[i][1]), str(reslist[i][2]), reslist[i][4]))
                count += reslist[i][2]
            self.bala_entry['text'] = str(count)

    # 余额修改窗口
    def fix_balance(self, balance):
        try:
            self.db.fix_balan(balance)
            last_balance = float(self.db.select_max())

            if last_balance - float(balance) < 0.01:
                self.top_information['text'] = '修改成功'
                self.bala_entry['text'] = balance
        except:
            self.top_information['text'] = '修改失败'

    # 屏幕刷新
    def refresh(self):
        if self.db.connect():
            self.top_information['text'] = '网络连接正常'
        else:
            self.top_information['text'] = '连接失败,请检查你的网络连接和数据库状态'
        self.cost_time.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        # try:
        #     self.bala_entry['text'] = self.db.select_max()
        # except:
        self.bala_entry['text'] = ' '
        self.first_time.set(time.strftime('%Y-%m-%d'))
        self.last_time.set(time.strftime('%Y-%m-%d'))
        self.cost_num.set('')
        self.remarks.set('')
        self.select_infor.set('')
        # 清空tree下内容
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def fix_ip(self, ip):
        pat = r'^(([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[.]){3}([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$'
        res = re.fullmatch(pat, ip)
        print(res)
        if res:
            if self.db.get_ip() == ip:
                self.top_information['text'] = '更改失败,IP未进行变化'
            else:
                self.top_information['text'] = '正在连接,请等待'
                self.db.close()
                self.db.set_ip(ip)
                self.db.connect()
                self.refresh()
        else:
            self.top_information['text'] = 'IP格式错误'


