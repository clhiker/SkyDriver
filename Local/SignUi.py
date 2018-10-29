from tkinter import *
import RegisterUi
import DriverUi
import Client


class SignUi():
    def __init__(self):
        self.root  = Tk()
        # 一大坑点，一定要是全局变量！！！！！！！！！！！
        # self.bm = PhotoImage(file='d:/logo.gif')
        self.username = None
        self.password = None

        self.is_error = False

    # 初始化窗口
    def setWindow(self):
        self.root.title('我的网盘')
        self.root.geometry('400x400')
        self.root.resizable(width=False, height=False)

    # 放置logo
    def setLogo(self):
        logo = Label(self.root,
                            #image=self.bm,
                            ).grid(row=0, column=0, columnspan=4)

    # 登录界面
    def setSignInput(self):
        Label(self.root,
                text='请输入用户名',
                ).grid(row=2, column=0)
        self.username_entry = Entry(self.root,
                                 width=15,
                                 )
        self.username_entry.grid(row=2,column=1,sticky=N+E+S+W)


        Label(self.root,
                text='请输入密码',
                ).grid(row=4, column=0)
        self.password_entry = Entry(self.root,
                              show='*'
                              )
        self.password_entry.grid(row=4, column=1, sticky=N+E+S+W)

    # 登录按钮
    def setSignInButton(self):
        Button(self.root,
                 text='登录',
                 command=self.signInResponse).grid(
                 row=6, column=1,sticky=N+E+S+W)

    # 登录信号槽
    def signInResponse(self):

        self.getInfoFromEntry()
        # 先检查是否用户名密码正确
        client = Client.Client()
        while not client.checkForUserAndPassword(self.username, self.password):
            self.is_error = True
            self.show()
            self.getInfoFromEntry()

        # 然后关闭当前窗口并生成新的窗口
        self.root.destroy()
        driver = DriverUi.DriverUi()
        driver.show()


    # 注册按钮
    def setRegisterButton(self):
        Button(self.root,
                  text='注册',
                  command=self.registerResponse).grid(
                  row=8, column=1, sticky=N+E+S+W)
    # 注册选项
    def registerResponse(self):
        self.root.destroy()
        register = RegisterUi.RegisterUi()
        register.show()

    # 显示输出
    def show(self):
        self.setLogo()
        if self.is_error :
            Label(self.root,
                  text='用户名或密码不正确，请重新输入',
                  foreground = 'red'
                  ).grid(row=1, column=0, columnspan=2)
        else:
            self.fillSpace(1)

        self.setSignInput()
        self.fillSpace(3)

        self.setSignInButton()
        self.fillSpace(5)

        self.setRegisterButton()
        self.fillSpace(7)

        self.root.mainloop()

    def fillSpace(self, row):
        fill_space = Label(self.root).grid(row=row, column=0, columnspan=4)

    #　从entry中获取数据
    def getInfoFromEntry(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

    # 首先应该检查网络连接
    def checkForCollect(self):
        pass


if __name__ == '__main__':
    SignUi().show()