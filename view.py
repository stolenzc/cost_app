#! /usr/bin/python
# -*- coding: utf8 -*-
import tkinter
from Mysqldb import Mydb
import time
from tkinter import ttk
import tkinter.messagebox
# import win32clipboard
from myFunction import my_function
import webbrowser
from icon import Icon
import base64
import os
# global version_id
version_id = '1.21'
# 1.01更新内容:更改作者名字
#  1.1更新内容:   1.更改软件主窗体左上角图标
#                 2.更改软件更新的链接复制,修改为直接打开浏览器进行下载
#                 3.新增软件使用说明
#                 4.重构软件底层代码,优化界面,按键输入框更符合扁平化界面
#                 5.添加网络ip更改
#                 6.修复软件刷新问题
#                 7.修复能够重复提交的问题
#                 8.尝试添加登录方式
# 1.2更新内容：   1.修改余额显示改为查询统计
#                 2.删除菜单栏中余额修改选项
#                 3.解决打开软件无法连接数据库后切换数据库失败的问题
#                 4.将软件说明页面转移到stolenzc.github.io/View/页面中去
#                 5.测试切换无效ip后卡死问题,该情况系正常现象,输入ip后系统会进行连接,需要时间
# 即将更改:
#                 1.数据库中删除余额项
#                 2.统计排序


class SecondWindow(object):
    def __init__(self, my_function):
        self.my_function = my_function

    # def balance_fix_window(self):
    #     fix_bala = tkinter.Toplevel()
    #     fix_bala.title('余额修改')
    #     with open('tmp.ico', 'wb') as tmp:
    #         tmp.write(base64.b64decode(Icon().img))
    #     fix_bala.iconbitmap('tmp.ico')
    #     os.remove('tmp.ico')
    #     # fix_bala.iconbitmap(r'.\\icon.ico')
    #     fix_bala.geometry('300x200+400+200')
    #     fix_bala.resizable(0, 0)
    #     var_balance = tkinter.Variable()
    #     label1 = tkinter.Label(fix_bala,
    #                            text='  ',
    #                            height=2,
    #                            )
    #     label1.pack()
    #     balance = ttk.Entry(fix_bala,
    #                         font=('黑体', 15),
    #                         width=10,
    #                         textvariable=var_balance,
    #                         )
    #     balance.pack()
    #     label2 = tkinter.Label(fix_bala,
    #                            text='  ',
    #                            height=2,
    #                            )
    #     label2.pack()
    #     button = ttk.Button(fix_bala,
    #                         text='确认修改',
    #                         command=lambda: self.my_function.fix_balance(var_balance.get()),
    #                         # font=('黑体', 15),
    #                         # justify='center',
    #                         )
    #     button.pack()
    #     fix_bala.mainloop()

    def check_update(self):
        sql = 'select version from version where id=(select max(id) from version)'
        result = db.select_sql(sql)
        if result[0] == version_id:
            tkinter.messagebox.showinfo('提示', '你的版本号为:' + version_id + '\n版本为最新,无需更新')
        elif float(result[0]) - float(version_id) > 0.01:
            yesno = tkinter.messagebox.askyesno('提示', '最新版本为:' + result[
                0] + ',点击确认进入浏\n览器开始下载')
            if yesno:
                webbrowser.open_new_tab('https://stolenzc.gitee.io/View/Download/view.rar')
        else:
            tkinter.messagebox.showinfo('提示', '你是内测版本,无需更新')

    def about_me(self):
        tkinter.messagebox.showinfo('提示', '作者:99\n版本号:' + version_id + '\nCopyright 2019 99 All rights Reserved.')

    # 数据库地址更改,容易造成软件卡死
    def fix_ip_window(self):
        fix_ip = tkinter.Toplevel()
        fix_ip.title('数据库IP修改')
        fix_ip.geometry('300x200+400+200')
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(Icon().img))
        fix_ip.iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        # fix_ip.iconbitmap(r'.\\icon.ico')
        fix_ip.resizable(0, 0)
        new_ip = tkinter.Variable()
        label1 = tkinter.Label(fix_ip,
                               text='  ',
                               height=2,
                               )
        label1.pack()
        balance = ttk.Entry(fix_ip,
                            font=('黑体', 15),
                            width=20,
                            textvariable=new_ip,
                            )
        balance.pack()
        label2 = tkinter.Label(fix_ip,
                               text='  ',
                               height=2,
                               )
        label2.pack()
        button = ttk.Button(fix_ip,
                            text='确认修改',
                            command=lambda: self.my_function.fix_ip(new_ip.get()),
                            # font=('黑体', 15),
                            # justify='center',
                            )
        button.pack()
        fix_ip.mainloop()

    def how_to_use(self):
        webbrowser.open_new_tab('https://stolenzc.gitee.io/View/')



class MainWindow(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.window_init()
        self.second_window = SecondWindow(self.myfunction)

        self.root.mainloop()

    def window_init(self):
        self.root.title('消费明细记录')
        with open('tmp.ico', 'wb') as tmp:
            tmp.write(base64.b64decode(Icon().img))
        self.root.iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        # self.root.iconbitmap(r'.\\icon.ico')
        self.root.geometry('800x530+260+60')
        self.root.resizable(0, 0)

        self.cost_time = tkinter.Variable()
        self.cost_num = tkinter.Variable()
        self.balance_num = tkinter.Variable()
        self.remarks = tkinter.Variable()
        self.first_time = tkinter.Variable()
        self.last_time = tkinter.Variable()
        self.select_infor = tkinter.Variable()

        self.frame_window = tkinter.Frame(self.root)
        self.window_insert()
        self.window_select()
        self.meun_bar()
        self.frame_window.pack(fill=tkinter.BOTH,
                               anchor='center')
        self.myfunction = my_function(self.top_information, self.cost_time, self.cost_num, self.bala_entry, self.remarks, self.first_time, self.last_time, self.select_infor, self.tree)
        # print(self.cost_time)
        # print(self.cost_num)
        # print(self.remarks)
        self.myfunction.init(db)

    def window_insert(self):
        frame1 = tkinter.Frame(self.frame_window)
        self.top_information = tkinter.Label(frame1,
                                             font=('黑体', 15),
                                             # bg='white',
                                             # width=50,
                                             justify='center')
        self.top_information.pack(expand=tkinter.YES,
                                  side='top',
                                  fill=tkinter.X,
                                  anchor='center')
        # self.top_information['text'] = '测试最大能够显示的字数第十二个字第十七个字第二十二个字'
        frame1_left = tkinter.Frame(frame1)
        frame1_right = tkinter.Frame(frame1)
        frame1_left_top = tkinter.Frame(frame1_left)
        frame1_left_bottom = tkinter.Frame(frame1_left)
        time_label = tkinter.Label(frame1_left_top,
                                   text='消费时间',
                                   # bg='white',
                                   fg='black',
                                   font=('黑体', 14),
                                   justify='center',
                                   anchor='center',
                                   height=2)
        time_label.pack(fill=tkinter.Y,
                        side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        time_entry = ttk.Entry(frame1_left_top,
                               textvariable=self.cost_time,
                               font=('黑体', 15),
                               width=20)
        time_entry.pack(side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )
        # times.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        cost_label = tkinter.Label(frame1_left_top,
                                   text=' 花费金额',
                                   # bg='white',
                                   fg='black',
                                   font=('黑体', 14),
                                   justify='center',
                                   anchor='center')
        cost_label.pack(fill=tkinter.Y,
                        side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        cost_entry = ttk.Entry(frame1_left_top,
                               textvariable=self.cost_num,
                               font=('黑体', 15),
                               width=10)
        cost_entry.pack(side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        bala_label = tkinter.Label(frame1_left_top,
                                   text=' 统计',
                                   # bg='white',
                                   fg='black',
                                   font=('黑体', 14),
                                   justify='center',
                                   anchor='center')
        bala_label.pack(fill=tkinter.Y,
                        side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        self.bala_entry = tkinter.Label(frame1_left_top,
                                        bg='#D3D3D3',
                                        font=('黑体', 15),
                                        width=10)
        self.bala_entry.pack(side=tkinter.LEFT,
                             expand=tkinter.YES,
                             )
        frame1_left_top.pack(fill=tkinter.X,
                             expand=tkinter.YES,
                             side='top',
                             )
        info_label = tkinter.Label(frame1_left_bottom,
                                   text='备注信息',
                                   # bg='white',
                                   # fg='black',
                                   font=('黑体', 14),
                                   justify='center',
                                   anchor='center',
                                   height=2)
        info_label.pack(fill=tkinter.Y,
                        side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        info_entry = ttk.Entry(frame1_left_bottom,
                               textvariable=self.remarks,
                               font=('黑体', 15),
                               width=57)
        info_entry.pack(side=tkinter.LEFT,
                        expand=tkinter.YES,
                        )

        frame1_left_bottom.pack(fill=tkinter.X,
                                expand=tkinter.YES,
                                side='bottom',
                                )
        frame1_left.pack(fill=tkinter.Y,
                         expand=tkinter.YES,
                         side='left')

        sure_button = ttk.Button(frame1_right,
                                 text='确认提交',
                                 command=lambda: self.myfunction.commit_fix(),
                                 # font=('黑体', 15),
                                 # style=font('黑体', 15),
                                 width=12,
                                 # state='disable'
                                 # height=4
                                 )
        ttk.Style().configure(".", font=("黑体", 15))
        sure_button.pack(fill=tkinter.BOTH,
                         expand=tkinter.YES,
                         anchor='center')

        frame1_right.pack(fill=tkinter.Y,
                          expand=tkinter.YES,
                          side='left')

        frame1.pack(
                    # side='top',
                    fill=tkinter.X,
                    expand=tkinter.YES,
                    anchor='n'
                    )

    def window_select(self):
        frame2 = tkinter.Frame(self.frame_window,
                               pady=20,padx=10)
        frame2_top = tkinter.Frame(frame2)
        frame2_bottom = tkinter.Frame(frame2)
        time_first_label = tkinter.Label(frame2_top,
                                         text='起始日期',
                                         # bg='white',
                                         fg='black',
                                         font=('黑体', 15),
                                         # justify='center',
                                         # anchor='center'
                                         )
        time_first_label.pack(side=tkinter.LEFT,
                              fill=tkinter.Y,
                              expand=tkinter.YES)

        time_first_entry = ttk.Entry(frame2_top,
                                     font=('黑体', 15),
                                     textvariable=self.first_time,
                                     width=12)
        time_first_entry.pack(side=tkinter.LEFT,
                              expand=tkinter.YES)

        time_last_label = tkinter.Label(frame2_top,
                                        text=' 终止日期',
                                        # bg='white',
                                        fg='black',
                                        font=('黑体', 15),
                                        # justify='center',
                                        # anchor='center'
                                        )
        time_last_label.pack(side=tkinter.LEFT,
                             fill=tkinter.Y,
                             expand=tkinter.YES)

        time_last_entry = ttk.Entry(frame2_top,
                                    textvariable=self.last_time,
                                    font=('黑体', 15),
                                    width=12)
        time_last_entry.pack(side=tkinter.LEFT,
                             expand=tkinter.YES)

        infor_label = tkinter.Label(frame2_top,
                                    text=' 备注查询',
                                    # bg='white',
                                    fg='black',
                                    font=('黑体', 15),
                                    height=2,
                                    # justify='center',
                                    # anchor='center'
                                    )
        infor_label.pack(side=tkinter.LEFT,
                         fill=tkinter.Y,
                         expand=tkinter.YES)

        infor_entry = ttk.Entry(frame2_top,
                                font=('黑体', 15),
                                textvariable=self.select_infor,
                                width=15)
        infor_entry.pack(side=tkinter.LEFT,
                         expand=tkinter.YES)

        select_button = ttk.Button(frame2_top,
                                   text='查询',
                                   command=lambda: self.myfunction.select_and_play(),
                                   # font=('黑体', 15),
                                   width=10)
        # ttk.Style().configure(".", font=("黑体", 15))
        select_button.pack(side=tkinter.LEFT,
                           fill=tkinter.Y,
                           expand=tkinter.YES)
        frame2_top.pack(side=tkinter.TOP,
                        fill=tkinter.X,
                        expand=tkinter.YES)

        self.tree = ttk.Treeview(frame2_bottom,
                                 show="headings",  # 隐藏首列
                                 # font=tkFont.Font(family='黑体', size=20),
                                 # font=15pix,
                                 height=15,
                                 # yscrollcommand=scrollBar.set
                                 )
        self.tree.pack(side='left',
                       fill=tkinter.Y,
                       expand=tkinter.YES)
        ttk.Style().configure("Treeview", font=("黑体", 13))
        # ttk.Treeview.configure("", font=("黑体", 10))
        self.tree['columns'] = ('序号', '消费时间', '消费金额', '备注')
        self.tree.column('序号', width=50, anchor='center')
        self.tree.column('消费时间', width=220, anchor='center')
        self.tree.column('消费金额', width=100, anchor='e')
        self.tree.column('备注', width=390)

        self.tree.heading('序号', text='序号')
        self.tree.heading('消费时间', text='消费时间')
        self.tree.heading('消费金额', text='消费金额')
        self.tree.heading('备注', text='备注')

        scroll_bar = tkinter.Scrollbar(frame2_bottom)

        scroll_bar.pack(side='right',
                        fill=tkinter.Y,
                        expand=tkinter.YES)
        scroll_bar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_bar.set)
        frame2_bottom.pack(side='top',
                           fill=tkinter.X,
                           expand=tkinter.YES)

        frame2.pack(
                    # side=tkinter.TOP,
                    fill=tkinter.X,
                    expand=tkinter.YES,
                    anchor='n'
                    )

    def meun_bar(self):
        menubar = tkinter.Menu(self.root,
                               # font=('黑体', 15),
                               bg='black'
                               )
        self.root.config(menu=menubar)
        menu1 = tkinter.Menu(menubar, tearoff=False)
        # menu1.add_command(label='余额修改', command=lambda: self.second_window.balance_fix_window())
        # menu1.add_separator()

        # 下个版本添加
        # menu1.add_command(label='数据库地址', command=lambda: self.second_window.fix_ip_window())
        # menu1.add_separator()
        menu1.add_command(label='屏幕刷新', command=lambda: self.myfunction.refresh())
        menu1.add_separator()
        menu1.add_command(label='退出', command=self.root.quit)
        menubar.add_cascade(label='菜单', menu=menu1)

        menu2 = tkinter.Menu(menubar, tearoff=False)
        menu2.add_command(label='检查更新', command=lambda: self.second_window.check_update())
        menu2.add_separator()
        menu2.add_command(label='使用说明', command=lambda: self.second_window.how_to_use())
        menu2.add_separator()
        menu2.add_command(label='关于我', command=lambda: self.second_window.about_me())
        menubar.add_cascade(label='关于软件', menu=menu2)


if __name__ == '__main__':
    # db = Mydb('192.168.0.106')
    # db = Mydb('10.7.185.72')
    db = Mydb('192.168.0.103')
    # db = Mydb('127.0.0.1')
    root = MainWindow()


