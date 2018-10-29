import configparser
from tkinter import *
import Local.Client
from Local import SignUi


class RegisterUi():

    #构造函数
    def __init__(self):
        self.root = Tk()
        #self.bm = PhotoImage(file='logo.gif')
        self.username = None
        self.password = None
        self.password_again = None
        self.server_address = None

    #初始化窗口
    def setWindow(self):
        self.root.title('网盘注册')
        self.root.geometry('400x400')  # 窗口大小
        self.root.resizable(width=False, height=False)  # 宽和高都设置为可变的

    # 设置logo图标
    def setLogo(self):
        logo = Label(self.root,
                            #image=self.bm,
                            ).grid(row=0, column=0, columnspan = 4)

    # 用户名
    def inputUsername(self):
        self.fillSpace(1)
        username_label = Label(self.root,
                                    text='请输入用户名',
                                    ).grid(row=2, column=0)

        self.username_entry = Entry(self.root,
                              )
        self.username_entry.grid(row=2, column=1)
    # 密码
    def inputPassword(self):
        self.fillSpace(3)
        password_label = Label(self.root,
                                    text='请输入密码',
                                    ).grid(row=4, column=0)

        self.password_entry = Entry(self.root,
                              show='*'
                              )
        self.password_entry.grid(row=4, column=1)

        self.fillSpace(5)
        password_again_label = Label(self.root,
                                    text='请再次输入密码',
                                    ).grid(row=6, column=0)
        self.password_again_entry = Entry(self.root,
                              show='*'
                              )
        self.password_again_entry.grid(row=6, column=1)
    # 服务器地址
    def inputAddress(self):
        self.fillSpace(7)
        server_address_label = Label(self.root,
                                          text='请输入服务器网址',
                                          ).grid(row=8, column=0)
        self.server_address_entry = Entry(self.root,
                                    )
        self.server_address_entry.grid(row=8, column=1)

        self.fillSpace(9)
    # 开始注册按钮
    def beginRegister(self):
        register_button = Button(self.root,
                                      text='注册',
                                      command=self.checkRegister
                                      ).grid(row=10, column=1,sticky=N+E+S+W)

    # 注册内容检查
    def checkRegister(self):
        self.getInfoFromEntry()
        # 1、密码检查
        while self.checkPassword():
            self.inputPassword()
            self.errorInformatioin()
            self.password = self.password_entry.get()
            self.password_again = self.password_again_entry.get()
        # 2、服务器地址检查
        self.checkServerAddress()

    # 密码检查
    def checkPassword(self):

        if self.password == self.password_again:
            return False
        else:
            return True

    # 服务器地址检查
    def checkServerAddress(self):
        address_list = self.server_address.split(':')
        ip = address_list[0]
        port = address_list[1]
        client = Local.Client.Client()

        while client.registerSocket((ip,int(port)), self.username, self.password):
            # 服务器地址出错，重写
            self.inputAddress()
            error_info = Label(self.root, text='服务器配置不正确请重新配置',
                               foreground='red', anchor='w'
                               ).grid(row=7, column=1, columnspan=4, sticky=W)
            self.server_address = self.server_address_entry.get()

        # 地址配置写入配置文件
        print('开始写入配置')
        config = configparser.ConfigParser()
        config.add_section('address')
        config.set('address','ip',ip)
        config.set('address','port',port)
        with open('local.ini','w+') as fw:
            config.write(fw)
        fw.close()
        self.root.destroy()
        ui = SignUi.SignUi()
        ui.show()


    # 打印密码不一致的错误信息
    def errorInformatioin(self):
        error_info = Label(self.root, text='密码输入不一致请重新输入',
                           foreground = 'red',anchor='w'
                            ).grid(row=3, column=1, columnspan=4,  sticky = W)

    # 添加空白，界面更整齐
    def fillSpace(self, row):
        fill_space = Label(self.root).grid(row=row, column=0, columnspan=4)

    # 从entry中读取数据
    def getInfoFromEntry(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.password_again = self.password_again_entry.get()
        self.server_address = self.server_address_entry.get()

    # 注册过程
    def register(self):
        self.inputUsername()
        self.inputPassword()
        self.inputAddress()
        self.beginRegister()



    def show(self):
        self.setWindow()
        self.setLogo()
        self.register()
        self.root.mainloop()


if __name__ == '__main__':
    RegisterUi().show()
