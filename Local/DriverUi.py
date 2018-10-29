'''
版本1.3
添加了文件下载能力
添加了上传下载的暂停取消功能
图标的小幅度修改
'''

from tkinter import *
import time
import os
import threading
import Local.UploadUi
import Local.Upload
import Local.Client

class DriverUi():
    #构造函数
    def __init__(self):
        self.root = Tk()
        self.page_record = []

        self.select_list = []
        self.isSelectAll = False
        self.frame1_3 = None

        # 上传队列
        self.upload_queue = []
        self.upload_frame_list = []
        
        self.download_queue = []
        self.download_frame_list = []

        self.dir_len = 0

        get_root_path_client = Local.Client.Client()
        self.root_path = get_root_path_client.getRootPathClient()
        self.now_path = self.root_path
        self.getImage()
    def getImage(self):
        self.dir_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep +'image' + os.sep + 'dir.gif')
        self.file_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep +'image' + os.sep + 'file.gif')
        self.home_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'home.gif')
        self.sort_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'sort.gif')
        self.flush_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'flush.gif')

    #初始化窗口
    def setWindow(self):
        self.root.title('我的网盘')
        # ui_width = 1000
        # ui_height = 500
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # driver_size = '%dx%d+%d+%d' % (ui_height, ui_height,
        #                                (screen_width - ui_width) / 2, (screen_height - ui_height) / 2)
        #
        # self.root.geometry(driver_size)  # 窗口大小
        # self.root.resizable(width=False, height=False)  # 宽和高都设置为可变的
        self.root.geometry('800x500')

        # 1、4个功能键
        self.canvas1 = Canvas(self.root)
        self.frame1 = Frame(self.canvas1)
        self.canvas1.pack(fill='both')
        self.canvas1.create_window((0, 0),window=self.frame1)
        self.frame1.pack(fill='both')
        self.chooseButton()

    # 功能选择按钮
    def chooseButton(self):
        Button(
            self.frame1, text='文件列表',width=28, command=self.showFileListPage
            ).grid(row=0, column=0, columnspan=5, sticky=N+E+S+W)

        Button(
            self.frame1, text='正在上传',width=28, command=self.uploadFilePage
            ).grid(row=0, column=5, columnspan=5, sticky=N+E+S+W)

        Button(
            self.frame1, text='正在下载',width=28, command=self.downloadFilePage
            ).grid(row=0, column=10, columnspan=5, sticky=N+E+S+W)

        Button(
            self.frame1, text='上传完成',width=28, command=self.finishUploadPage
            ).grid(row=0, column=15, columnspan=5, sticky=N+E+S+W)

    # 第1个，文件列表页面
    def showFileListPage(self):
        # 首先检查之前页面的信息，并删除之前的页面
        if len(self.page_record) != 0:
            for item in self.page_record[0]:
                item.destroy()
            for item in self.page_record[1]:
                item.destroy()
            del self.page_record[0]
            del self.page_record[0]

        # 1、页面功能键
        self.canvas1_1 = Canvas(self.root)
        self.frame1_1 = Frame(self.canvas1_1)
        self.canvas1_1.pack(fill='both')
        self.canvas1_1.create_window((0, 0), window=self.frame1_1)
        self.frame1_1.pack(fill='both')
        self.keyOfFileList()

        # 2、文件信息展示栏
        self.canvas1_2 = Canvas(self.root)
        self.frame1_2 = Frame(self.canvas1_2)
        self.canvas1_2.pack(fill='both')
        self.canvas1_2.create_window((0, 0), window=self.frame1_2)
        self.frame1_2.pack(fill='both')
        self.showFileInfo()

        self.page_record.append([self.frame1_1, self.frame1_2])
        self.page_record.append([self.canvas1_1, self.canvas1_2])

        # 3、页面信息
        self.showObjectPageInNowPath(self.now_path)


    # 展示当前文件夹下的所有项
    def showObjectPageInNowPath(self, now_path):
        self.canvas1_3 = Canvas(self.root)
        self.frame1_3 = Frame(self.canvas1_3)
        self.vsb1 = Scrollbar(self.root, command=self.canvas1_3.yview)
        self.canvas1_3.configure(yscrollcommand=self.vsb1.set)
        self.canvas1_3.bind('<MouseWheel>')
        self.vsb1.pack(side="right", fill="y")
        self.canvas1_3.pack(fill='both')
        self.canvas1_3.create_window((4, 4), window=self.frame1_3, anchor="nw",
                                     tags="self.frame")
        self.frame1_3.bind("<Configure>", self.OnFrameConfigure1_3)

        # 将当前页面记录在案
        self.page_record[0].append(self.frame1_3)
        self.page_record[1].append(self.canvas1_3)
        self.page_record[1].append(self.vsb1)

        self.showObjectListPage()

    # 第2个，上传页面
    def uploadFilePage(self):
        if len(self.page_record) != 0:
            for item in self.page_record[0]:
                item.destroy()
            for item in self.page_record[1]:
                item.destroy()
            del self.page_record[0]
            del self.page_record[0]

        self.canvas2_1 = Canvas(self.root)
        self.frame2_1 = Frame(self.canvas2_1)
        self.canvas2_1.pack(fill='both')
        self.canvas2_1.create_window((0, 0), window=self.frame2_1)
        self.frame2_1.pack(fill='both')

        self.page_record.append([self.frame2_1])
        self.page_record.append([self.canvas2_1])

        self.uploadStatusDisplayBar()
        self.uploadFileProcessPage()


    # 上传任务栏
    def uploadStatusDisplayBar(self):
        residual_task = len(self.upload_queue)
        residual_task_label = Label(self.frame2_1,
                                    text='剩余任务：' + str(residual_task),
                                    ).grid(row=1, column=0, columnspan=5, sticky=N + E + S + W)

        all_start_button = Button(
            self.frame2_1, text='全部开始', font=15, command=self.allStartTasks
        ).grid(row=1, column=5, columnspan=5, sticky=N + E + S + W)

        all_stop_button = Button(
            self.frame2_1, text='全部暂停', font=15, command=self.allStopTasks
        ).grid(row=1, column=10, columnspan=5, sticky=N + E + S + W)

        all_cancel_button = Button(
            self.frame2_1, text='全部取消', font=15, command=self.allCancelTasks
        ).grid(row=1, column=15, columnspan=5, sticky=N + E + S + W)


    # 上传文件进程页面
    def uploadFileProcessPage(self):
        self.canvas2_2 = Canvas(self.root)
        self.frame2_2 = Frame(self.canvas2_2)
        self.vsb2 = Scrollbar(self.root, command=self.canvas2_2.yview)
        self.canvas2_2.configure(yscrollcommand=self.vsb2.set)
        self.canvas2_2.bind('<MouseWheel>')
        self.vsb2.pack(side="right", fill="y")
        self.canvas2_2.pack(fill='both')
        self.canvas2_2.create_window((4, 4), window=self.frame2_2, anchor="nw",
                                     tags="self.frame")
        self.frame2_2.bind("<Configure>", self.OnFrameConfigure2_2)

        # 将当前页面记录在案
        self.page_record[0].append(self.frame2_2)
        self.page_record[1].append(self.canvas2_2)
        self.page_record[1].append(self.vsb2)
        self.showFileUploadListPage()

    def showFileUploadListPage(self):
        index = 0
        for item in self.upload_queue:
            file_path = item[0]
            # 从程序中获取的分隔符是/
            filename = file_path[file_path.rfind('/') + 1 : ]
            frame_line = Frame(self.frame2_2)
            frame_line.pack()

            id = index

            # 本地文件可以获取文件大小
            file_size = self.modifySizeNameFromFile(item[0])
            self.showUploadFileLine(id, filename, file_size, index, item[1], frame_line)
            index += 1

    # 上传的进度条一栏
    def showUploadFileLine(self, id, filename, file_size, index, upload_client, frame_line):
        upload_status = True
        Label(frame_line,
              text='文件',
              ).grid(row=index, column=0, columnspan=2)
        Label(frame_line,
              text=filename,
              ).grid(row=index, column=2, columnspan=8)
        Label(frame_line,
              text=file_size,
              ).grid(row=index, column=10, columnspan=2)
        # 进度条
        t = threading.Thread(target=self.uploadProcessBar, args=(id, index, upload_client, frame_line))
        t.start()
        # 上传状态信息

        self.uploadStatus(id, filename, upload_status, index, frame_line, upload_client)

    # 进度条
    def uploadProcessBar(self, id, index, upload_client, frame_line):
        var = StringVar()
        var.set("0%")
        Label(frame_line, textvariable=var, width=5).grid(row=index, column=15)

        # 创建一个背景色为白色的矩形
        canvas = Canvas(frame_line, width=70, height=20, bg="white")
        # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
        canvas.create_rectangle(2, 2, 180, 27, width=1, outline="black")
        canvas.grid(row=index, column=12, ipadx=3)
        fill_line = canvas.create_rectangle(2, 2, 0, 27, width=0, fill="blue")

        while True:
            process = upload_client.getLoadProcess()
            canvas.coords(fill_line, (0, 0, process, 30))
            var.set(str(process) + "%")
            canvas.update()
            time.sleep(0.01)
            if process == 100:
                self.cancelUploadPage(id,frame_line, upload_client)
                break
    def cancelUploadPage(self, id, frame_line, upload_client):
        frame_line.destroy()
        self.upload_queue.remove(self.upload_queue[id])
        self.uploadFilePage()

    def cancelUploadResponse(self, id, filename, frame_line, upload_client):
        cancel_client = Local.Client.Client()
        cancel_client.deleteFileClient(filename)
        upload_client.setCancelButton(True)
        frame_line.destroy()
        self.upload_queue.remove(self.upload_queue[id])
        self.uploadFilePage()

    # 停止下载
    def stopUploadResponse(self,id, filename,  upload_client, upload_status, index, frame_line):
        upload_status = False
        upload_client.setStopButton(True)
        self.uploadStatus(id, filename, upload_status, index, frame_line, upload_client)

    # 开始下载
    def startUploadResponse(self,id, filename, upload_client, upload_status, index, frame_line):
        upload_status = True
        upload_client.setStopButton(False)
        self.uploadStatus(id,filename, upload_status, index, frame_line, upload_client)
        
    # 上传状态
    def uploadStatus(self,id, filename, upload_status, index, frame_line, upload_client):
        if upload_status:
            Label(frame_line,
                  text='正在上传',
                  ).grid(row=index, column=16, columnspan=2)
        else:
            Label(frame_line,
                  text=' 已暂停 ',
                  ).grid(row=index, column=16, columnspan=2)
        # 暂停，开启按钮
        if upload_status:
            Button(frame_line, text='‖', command=lambda: self.stopUploadResponse(
                id,filename, upload_client, upload_status, index, frame_line)
                   ).grid(row=index, column=18, columnspan=1)
        else:
            Button(frame_line, text='▷', command=lambda: self.startUploadResponse(
                id,filename, upload_client, upload_status, index, frame_line)
                   ).grid(row=index, column=18, columnspan=1)
        # 取消按钮
        Button(frame_line, text='×', command=lambda: self.cancelUploadResponse(
            id,filename, frame_line, upload_client)
               ).grid(row=index, column=19, columnspan=1)

        
    # 3、下载页面
    def downloadFilePage(self):
        if len(self.page_record) != 0:
            for item in self.page_record[0]:
                item.destroy()
            for item in self.page_record[1]:
                item.destroy()
            del self.page_record[0]
            del self.page_record[0]

        self.canvas3_1 = Canvas(self.root)
        self.frame3_1 = Frame(self.canvas3_1)
        self.canvas3_1.pack(fill='both')
        self.canvas3_1.create_window((0, 0), window=self.frame3_1)
        self.frame3_1.pack(fill='both')

        self.page_record.append([self.frame3_1])
        self.page_record.append([self.canvas3_1])

        self.downloadStatusDisplayBar()
        self.downloadFileProcessPage()
        
    # 下载页面展示栏
    def downloadStatusDisplayBar(self):
        residual_task = len(self.download_queue)
        Label(self.frame3_1,
            text='剩余任务：' + str(residual_task),
            ).grid(row=1, column=0, columnspan=5, sticky=N + E + S + W)

        Button(
            self.frame3_1, text='全部开始', font=15, command=self.allStartTasks
            ).grid(row=1, column=5, columnspan=5, sticky=N + E + S + W)

        Button(
                self.frame3_1, text='全部暂停', font=15, command=self.allStopTasks
            ).grid(row=1, column=10, columnspan=5, sticky=N + E + S + W)

        Button(
                self.frame3_1, text='全部取消', font=15, command=self.allCancelTasks
            ).grid(row=1, column=15, columnspan=5, sticky=N + E + S + W)

    # 下载文件进程页面
    def downloadFileProcessPage(self):
        self.canvas3_2 = Canvas(self.root)
        self.frame3_2 = Frame(self.canvas3_2)
        self.vsb3 = Scrollbar(self.root, command=self.canvas3_2.yview)
        self.canvas3_2.configure(yscrollcommand=self.vsb3.set)
        self.canvas3_2.bind('<MouseWheel>')
        self.vsb3.pack(side="right", fill="y")
        self.canvas3_2.pack(fill='both')
        self.canvas3_2.create_window((4, 4), window=self.frame3_2, anchor="nw",
                                     tags="self.frame")
        self.frame3_2.bind("<Configure>", self.OnFrameConfigure3_2)

        # 将当前页面记录在案
        self.page_record[0].append(self.frame3_2)
        self.page_record[1].append(self.canvas3_2)
        self.page_record[1].append(self.vsb3)
        self.showFileDownloadListPage()

    def showFileDownloadListPage(self):
        index = 0
        for item in self.download_queue:
            filename = item[0][item[0].rfind(os.sep) + 1:]
            frame_line = Frame(self.frame3_2)
            frame_line.pack()
            # 下载文件需要远程获取文件大小
            file_size = self.modifySizeNameFromSize(item[1].getRemoteFileSize())

            self.showDownloadFileLine(filename, file_size, index, item[1], frame_line)
            index += 1

    # 下载的进度一栏
    def showDownloadFileLine(self, filename, file_size, index, download_client, frame_line):
        download_status = True
        Label(frame_line,
              text='文件',
              ).grid(row=index, column=0, columnspan=2)
        Label(frame_line,
              text=filename,
              ).grid(row=index, column=2, columnspan=8)
        Label(frame_line,
              text=file_size,
              ).grid(row=index, column=10, columnspan=2)
        # 进度条
        t = threading.Thread(target=self.downloadProcessBar, args=(index, download_client, frame_line))
        t.start()


        # 下载状态信息
        self.downloadStatus(download_status, index, frame_line, download_client)

    # 下载进度条
    def downloadProcessBar(self, index, download_client, frame_line):
        var = StringVar()
        var.set("0%")
        Label(frame_line, textvariable=var, width=5).grid(row=index, column=15)

        # 创建一个背景色为白色的矩形
        canvas = Canvas(frame_line, width=70, height=20, bg="white")
        # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色
        canvas.create_rectangle(2, 2, 180, 27, width=1, outline="black")
        canvas.grid(row=index, column=12, ipadx=3)
        fill_line = canvas.create_rectangle(2, 2, 0, 27, width=0, fill="blue")

        while True:
            process = download_client.getLoadProcess()
            if int(process) >= 100:
                process = 100
            canvas.coords(fill_line, (0, 0, process, 30))
            var.set(str(process) + "%")
            canvas.update()
            time.sleep(0.01)
            if process == 100:
                self.cancelDownloadResponse(download_client, frame_line)
                break
    # 取消下载
    def cancelDownloadResponse(self, download_client, frame_line):
        download_client.setCancelButton(True)
        frame_line.destroy()
        self.download_queue.remove(self.download_queue[0])
        self.downloadFilePage()

    # 停止下载
    def stopDownloadResponse(self, download_client, download_status, index, frame_line):
        download_status = False
        download_client.setStopButton(True)
        self.downloadStatus(download_status, index, frame_line, download_client)

        # 开始下载
    def startDownloadResponse(self, download_client, download_status, index, frame_line):
        download_status = True
        download_client.setStopButton(False)
        self.downloadStatus(download_status, index, frame_line, download_client)



        # 下载状态
    def downloadStatus(self, download_status, index, frame_line, download_client):

        if download_status:
            Label(frame_line,
                  text='正在下载',
                  ).grid(row=index, column=16, columnspan=2)
        else:
            Label(frame_line,
                  text=' 已暂停 ',
                  ).grid(row=index, column=16, columnspan=2)

        # 暂停，开启按钮
        if download_status:
            Button(frame_line, text='‖', command=lambda: self.stopDownloadResponse(
                download_client, download_status, index, frame_line)
                   ).grid(row=index, column=18, columnspan=1)
        else:
            Button(frame_line, text='▷', command=lambda: self.startDownloadResponse(
                download_client, download_status, index, frame_line)
                   ).grid(row=index, column=18, columnspan=1)

        # 取消按钮
        Button(frame_line, text='×', command=lambda: self.cancelDownloadResponse(download_client,frame_line)
               ).grid(row=index, column=19, columnspan=1)



    # 上传完成页面

    # 完成上传页面
    def finishUploadPage(self):
        if len(self.page_record) != 0:
            for item in self.page_record[0]:
                item.destroy()
            for item in self.page_record[1]:
                item.destroy()
            del self.page_record[0]
            del self.page_record[0]

        self.canvas4_1 = Canvas(self.root)
        self.frame4_1 = Frame(self.canvas4_1)
        self.canvas4_1.pack(fill='both')
        self.canvas4_1.create_window((0, 0), window=self.frame4_1)
        self.frame4_1.pack(fill='both')

        self.page_record.append([self.frame4_1])
        self.page_record.append([self.canvas4_1])

        self.finishUploadStatusDisplayBar()

    # 1、文件列表页面的功能键
    def keyOfFileList(self):
        self.functionalButton()
        self.showFilePathLabel()
        self.sortFileFromList()

    # 搜索文件文本框和按钮
    def sortFileFromList(self):
        self.search_context = Text(self.frame1_1,
                            background='lavender',
                            font=1,
                            width=20,
                            height=1
                            ).grid(row=1,column=15, columnspan=4)
        Button(
                self.frame1_1,image=self.sort_image, font=15, command=self.returnPreviousPage
                ).grid(row=1, column=19)
    # 展示文件路径标签
    def showFilePathLabel(self):
        input_label = Label(self.frame1_1,
                            text='我的网盘:/',
                            bg='pink',
                            font=('Arial', 12),
                            width=50, height=1
                            ).grid(row=1, column=5, columnspan=10)
    # 1、功能按钮
    def functionalButton(self):
        Button(
            self.frame1_1, text='<', font=15, command=self.returnPreviousPage
            ).grid(row=1, column=0)
        Button(
            self.frame1_1, image=self.flush_image, font=15, command=self.flush
            ).grid(row=1, column=2)
        Button(
            self.frame1_1, image = self.home_image, font=15, command=self.goHomePage
            ).grid(row=1, column=3)
        Button(
            self.frame1_1, text='□', font=15, command=self.selectAll
            ).grid(row=1, column=4)

        # 多级菜单上传按钮
        upload_button = Menubutton(
            self.frame1_1, text='上传', font=15
        )
        upload_button.grid(row=1, column=1)
        upload_button.menu = Menu(upload_button)
        upload_button.menu.add_command(label='上传文件', command=self.uploadFileResponse)
        upload_button.menu.add_command(label='上传文件夹', command=self.uploadDirResponse)
        upload_button['menu'] = upload_button.menu

        pass

    # 2、文件信息展示栏
    def showFileInfo(self):
        # 全选按钮
        Button(
                self.frame1_2, text='□', command=self.selectAll
                ).grid(row=2, column=0, sticky=N+E+S+W)
        # 文件名标识（标签）
        Label(self.frame1_2,
                text='文件名↓',
                ).grid(row=2, column=1, padx = 10, columnspan=9, sticky=N+E+S+W)
        # 文件大小展示标识
        Label(self.frame1_2,
                text='大小',
                ).grid(row=2, column=10, padx = 10, columnspan=5, sticky=N+E+S+W)
        # 修改时间标识
        Label(self.frame1_2,
                text='修改时间↓',
                ).grid(row=2, column=15, padx = 10, columnspan=5, sticky=N+E+S+W)

    # 3、文件页面展示
    def showObjectListPage(self):
        object_list = []
        dir_info = []
        file_info = []
        show_page_list_client = Local.Client.Client()
        show_page_list_client.getFilePathStruct(self.now_path, self.dir_len, dir_info, file_info)

        i = 0

        # 文件文件名输出
        for item in dir_info:
            self.show_dir_line(i, item[0], item[1])
            i += 1
        for item in file_info:
            self.show_file_line(i, item[0], item[1], item[2])
            i+=1
        
    # 文件夹栏目一行的消息
    def show_dir_line(self, index, dir_name, modify_time):
        # 选中信号
        Button(
                self.frame1_3, text='□', command= lambda : self.selectOne(index)
                ).grid(row=index, column=0)
        # 文件夹标识
        Label(self.frame1_3,
                image=self.dir_image
                ).grid(row=index, column=1)
        # 文件夹打开按钮
        dir_open_button = Button(self.frame1_3,
                                 text=dir_name,
                                 anchor=W
                                )
        # 绑定打开文件夹
        dir_open_button.bind('<Double-Button-1>', self.openDirHandlerAdaptor(
            self.openDir, relay_path=dir_name))
        # 绑定右键事件
        dir_open_button.bind("<Button-3>", lambda x: self.dirRightKeyMenu(x, dir_name))  # 绑定右键鼠标事件
        # 布局
        dir_open_button.grid(row=index, column=2, columnspan=8, sticky=N+E+S+W)

        # 大小标签
        Label(self.frame1_3,
              anchor=W,
                text='--',
                ).grid(row=index, column=10, columnspan=5)
        # 修改时间
        Label(self.frame1_3,
              anchor=W,
                text=modify_time,
                ).grid(row=index, column=15, columnspan=5)


    # 文件栏目一行的消息
    def show_file_line(self, index, filename, file_size, modify_time):
        # 选中信号
        Button(
            self.frame1_3, text='□', command= lambda : self.selectOne(index)
            ).grid(row=index, column=0)

        # 文件夹标识
        Label(self.frame1_3,
              image = self.file_image,
              ).grid(row=index, column=1)
        # 文件选中单击按钮
        file_open_button = Button(
            self.frame1_3, text=filename, anchor=W, command= lambda : self.selectOne(index))

        # 绑定右键事件
        file_open_button.bind("<Button-3>", lambda x: self.fileRightKeyMenu(x, filename))  # 绑定右键鼠标事件


        file_open_button.grid(row=index, column=2, columnspan=8,sticky=N+E+S+W)

        Label(self.frame1_3,
               text=file_size,
               anchor=W
               ).grid(row=index, column=10,  columnspan=5)
        # 修改时间
        Label(self.frame1_3,
              text=modify_time,
              anchor=W
              ).grid(row=index, column=15, columnspan=5)

    # 中间适配器
    def openDirHandlerAdaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    # 打开文件夹
    def openDir(self, event, relay_path):
        self.removeFileListPage()
        self.now_path = self.now_path + os.sep + relay_path
        self.showObjectPageInNowPath(self.now_path)
        # 取消勾选
        self.isSelectAll = True
        self.selectAll()

    # 每一行的单选信号
    def selectOne(self, index):
        if index in self.select_list:
            select_one_none_button = Button(
                self.frame1_3, text='□', command=lambda: self.selectOne(index)
            ).grid(row=index, column=0)
            self.select_list.remove(index)
        else:
            select_one_none_button = Button(
                        self.frame1_3, text='☑', command= lambda : self.selectOne(index)
                        ).grid(row=index, column=0)
            self.select_list.append(index)

    # 全选信号
    def selectAll(self):
        if self.isSelectAll:
            # 取消全选按钮
            create_new_folder_button = Button(
                self.frame1_1, text='□', font=15, command=self.selectAll
            ).grid(row=1, column=4)

            # 将之下的所有文件取消勾选
            for index in range(self.dir_len):
                select_one_none_button = Button(
                    self.frame1_3, text='□', command=lambda: self.selectOne(index)
                ).grid(row=index, column=0)
            self.isSelectAll = False

        else:
            # 点上全选按钮
            create_new_folder_button = Button(
                self.frame1_1, text='☑', font=15, command=self.selectAll
            ).grid(row=1, column=4)

            # 将之下的所有文件勾选
            for index in range(self.dir_len):
                select_one_none_button = Button(
                    self.frame1_3, text='☑', command=lambda: self.selectOne(index)
                ).grid(row=index, column=0)
            self.isSelectAll = True

    # 文件夹右键菜单
    def dirRightKeyMenu(self, event, dir_name):

        menu_bar = Menu(self.frame1_3, tearoff=False)  # 创建一个菜单
        menu_bar.delete(0, END)

        # 右键功能要有：下载，打开，删除，重命名，移动，属性
        menu_bar.add_command(label='下载')
        menu_bar.add_command(label='打开', command =lambda :self.openDir(event, dir_name))
        menu_bar.add_command(label='删除', command =lambda : self.deleteDirResponse(event, dir_name))
        menu_bar.add_command(label='重命名')
        menu_bar.add_command(label='移动')
        menu_bar.add_command(label='属性')

        menu_bar.post(event.x_root, event.y_root)

    # 删除文件夹
    def deleteDirResponse(self,event, delete_dir):
        delete_dir_client = Local.Client.Client()
        delete_dir_client.deleteDirClient(delete_dir)
        self.flush()

    # 重命名文件夹
    def renameDir(self):
        pass

    # 文件右键菜单
    def fileRightKeyMenu(self, event, filename):
        menu_bar = Menu(self.frame1_3, tearoff=False)  # 创建一个菜单
        menu_bar.delete(0, END)

        # 右键功能要有：下载，打开，删除，重命名，移动，属性
        menu_bar.add_command(label='下载', command = lambda : self.downLoadFileResponse(event, filename))
        menu_bar.add_command(label='删除', command =lambda : self.deleteFileResponse(event, filename))
        menu_bar.add_command(label='重命名')
        menu_bar.add_command(label='移动')

        menu_bar.post(event.x_root, event.y_root)

    # 下载文件
    def downLoadFileResponse(self, event, filename):
        # 先选择下载目的文件夹
        upload_ui = Local.UploadUi.SelectDir()
        self.root.wait_window(upload_ui)
        save_path = upload_ui.getDir()
        save_path = save_path + os.sep + filename

        download_client = Local.Client.Client()
        t = threading.Thread(target=download_client.downloadFile, args=(
             filename, save_path))
        t.start()

        self.download_queue.append([save_path, download_client])

        pass
    # 删除文件
    def deleteFileResponse(self, event, delete_file):
        delete_file_client = Local.Client.Client()
        delete_file_client.deleteFileClient(delete_file)
        self.flush()

    # 重命名文件
    def renameFile(self):
        pass



    def allStartTasks(self):
        pass
    def allStopTasks(self):
        pass
    def allCancelTasks(self):
        pass


    # 上传完成展示栏
    def finishUploadStatusDisplayBar(self):
        residual_task = ""
        residual_task_label = Label(self.frame4_1,
                                    text='' + residual_task,
                                    ).grid(row=1, column=0, columnspan=15, sticky=N + E + S + W)

        all_start_button = Button(
            self.frame4_1, text='清除所有记录', font=15, command=self.allStartTasks
        ).grid(row=1, column=15, columnspan=5, sticky=N + E + S + W)

    # < 按钮
    def returnPreviousPage(self):
        if self.now_path == self.root_path:
            return
        index = self.now_path.rfind(os.sep)
        self.now_path = self.now_path[:index]
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path) 

    # 上传文件按钮响应函数

    # 上传文件夹按钮
    def uploadDirResponse(self):
        upload_ui = Local.UploadUi.UploadUi()
        upload_dir_name = upload_ui.getDir()

        to_upload = Local.Upload.Upload()
        to_upload.upload_dir(upload_dir_name)

    # 上传文件按钮
    def uploadFileResponse(self):
        # 首先获取文件名
        upload_ui = Local.UploadUi.SelectFile()
        self.root.wait_window(upload_ui)
        file_path = upload_ui.getFile()

        if file_path.find('/') != -1:
            filename = file_path[file_path.rfind('/') + 1:]
        else:
            filename = file_path[file_path.rfind('\\') + 1:]

        upload_client = Local.Client.Client()
        t = threading.Thread(target=upload_client.upload, args=(
            self.now_path, filename, file_path))
        t.start()
        # 然后开始上传
        self.upload_queue.append([file_path, upload_client])


    # @ 刷新按钮
    def flush(self):
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path)
    # ^回到顶部按钮
    def goHomePage(self):
        if self.now_path == self.root_path:
            return
        self.now_path = self.root_path
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path)
    # 调整文件大小的表达
    def modifySizeNameFromFile(self, object_path):
        file_size = os.path.getsize(object_path)
        if file_size > 1024:
            file_size = file_size / 1024
            if file_size > 1024:
                file_size = file_size / 1024
                if file_size > 1024:
                    file_size = file_size / 1024
                    file_size = str(round(file_size,2)) + 'GB'

                else:
                    file_size = str(round(file_size,2)) + 'MB'
            else:
                file_size = str(round(file_size,2)) + 'KB'
        else:
            file_size = str(round(file_size,2)) + 'B'

        return  file_size

    def modifySizeNameFromSize(self, file_size):
        if file_size > 1024:
            file_size = file_size / 1024
            if file_size > 1024:
                file_size = file_size / 1024
                if file_size > 1024:
                    file_size = file_size / 1024
                    file_size = str(round(file_size,2)) + 'GB'

                else:
                    file_size = str(round(file_size,2)) + 'MB'
            else:
                file_size = str(round(file_size,2)) + 'KB'
        else:
            file_size = str(round(file_size,2)) + 'B'

        return  file_size
    # 调整修改时间
    def timeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    # 配置滚轮
    def OnFrameConfigure1_3(self, event):
        self.canvas1_3.configure(scrollregion=self.canvas1_3.bbox("all"))
    def OnFrameConfigure2_2(self, event):
        self.canvas2_2.configure(scrollregion=self.canvas2_2.bbox("all"))

    def OnFrameConfigure3_2(self, event):
        self.canvas3_2.configure(scrollregion=self.canvas3_2.bbox("all"))

    def removeFileListPage(self):
        if self.frame1_3 != None:
            self.frame1_3.destroy()
            self.canvas1_3.destroy()
            self.vsb1.destroy()

    def show(self):
        self.setWindow()
        self.chooseButton()  # 选择页面按钮
        self.showFileListPage()
        self.root.mainloop()

if __name__ == '__main__':
    driver = DriverUi()
    driver.show()