
# -*- coding: utf-8 -*-
import socket
import time
import configparser
import threading
import os


class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 读取配置文件
        self.readConfig()
        self.root_path = 'home'
        self.now_path = self.root_path
        # 绑定地址
        self.server_socket.bind(self.address)
        # 最多三台设备
        self.server_socket.listen(int(self.max_supported_devices))

    #
    def getImage(self):
        self.dir_image = 'image/dir.gif'

    # 读取配置信息
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config.get('address', 'ip')
        port = config.get('address', 'port')
        self.address = (ip, int(port))
        self.max_supported_devices = config.get('config', 'max_supported_devices')

    # 检查登录信息
    def checkForUsernameAndPassword(self, client):
        client.send('begin_check_for_username_and_password'.encode())
        username = client.recv(1024).decode()
        password = client.recv(1024).decode()

        remote = open("remote.txt")
        while 1:
            line = remote.readline()
            if not line:
                break

            username_line = line.replace('\n','',1)
            if username_line == username:
                line = remote.readline()
                password_line = line.replace('\n','',1)
                if password_line == password:
                    client.send('username_and_password_are_ok'.encode())
            else:
                line = remote.readline()

        client.send('username or password is error'.encode())

    # 服务器端查询注册信息
    def RegisterOnServer(self, client):
        client.send('connect_ok'.encode())
        username = client.recv(1024).decode()
        password = client.recv(1024).decode()
        with open('remote.txt', 'w') as f:
            f.writelines(username)
            f.write('\n')
            f.writelines(password)
            f.write('\n')
        f.close()

    # 上传选项
    # 接受数据线程
    def uploadFile(self, client):
        now_path = client.recv(1024).decode()
        filename = client.recv(1024).decode()
        file_path = now_path + os.sep + filename

        while True:
            data = client.recv(1024)
            if not data:
                break
            else:
                with open(file_path, 'ab') as f:
                    f.write(data)

        client.close()
        print('receive finished')

    # 获取文件路径结构
    def getFilePathStruct(self, client):
        client.send('connect_ok'.encode())
        up_path = client.recv(1024).decode()
        self.now_path = self.transPath(up_path)

        object_list = os.listdir(self.now_path)
        client.send(str(len(object_list)).encode())
        # 这些要放在服务器端
        for index in range(len(object_list)):       # 遍历文件夹
            object_path = os.path.join(self.now_path, object_list[index]).encode('utf-8')

            if os.path.isdir(object_path):   # 判断是否是文件夹，不是文件夹才打开
                client.send('0'.encode())
                time.sleep(0.002)
                dir_name = object_list[index]
                change_time = self.timeStampToTime(os.path.getmtime(object_path))
                client.send(dir_name.encode())
                time.sleep(0.002)
                client.send(change_time.encode())
                time.sleep(0.002)
            else:
                client.send('1'.encode())
                time.sleep(0.002)
                dir_name = object_list[index]
                file_size = self.modifySizeName(object_path)
                change_time = self.timeStampToTime(os.path.getmtime(object_path))
                client.send(dir_name.encode())
                time.sleep(0.002)
                client.send(file_size.encode())
                time.sleep(0.002)
                client.send(change_time.encode())
                time.sleep(0.002)

    # 删除文件夹
    def deleteDirServer(self, client):
        client.send('connect_ok'.encode())
        delete_dir = client.recv(1024).decode()
        delete_dir = self.now_path + os.sep + delete_dir
        os.removedirs(delete_dir)
        print(delete_dir)
    # 删除文件
    def deleteFileServer(self, client):
        client.send('connect_ok'.encode())
        delete_file = client.recv(1024).decode()
        delete_file = self.now_path + os.sep + delete_file
        os.remove(delete_file)
        print(delete_file)
    # 发送根目录信息
    def sendRootFileServer(self, client):
        client.send('connect_ok'.encode())
        time.sleep(0.02)
        client.send(self.root_path.encode())

    # 下载选项
    def downloadFileServer(self, client):
        download_filename = client.recv(1024).decode()
        file_path = self.now_path + os.sep + download_filename

        # 发送文件的实际大小
        client.send(str(os.path.getsize(file_path)).encode())
        time.sleep(0.002)

        with open(file_path, 'rb') as f:
            for line in f:
                client.send(line)
                # cancel = client.recv(1024).decode()
                # if cancel == 'cancel':
                #     print(cancel)
                #     break
        f.close()

    # 接收状态选项
    def receiveState(self, client, receive_info):
        print(receive_info)
        # 检查连接状态
        # 注册
        if receive_info == 'connecting':
            self.RegisterOnServer(client)
        # 登录
        if receive_info == 'check_for_username_and_password':
            self.checkForUsernameAndPassword(client)
        # 上传文件
        if receive_info == 'begin_to_upload_file':
            self.uploadFile(client)
        # 上传文件夹
        if receive_info == 'begin_to_upload_dir':
            pass
        # 获取文件路径结构
        if receive_info == 'ask_for_file':
            self.getFilePathStruct(client)
        if receive_info == 'delete_dir':
            self.deleteDirServer(client)
        if receive_info == 'delete_file':
            self.deleteFileServer(client)
        if receive_info == 'root_path':
            self.sendRootFileServer(client)
        if receive_info == 'download_file':
            self.downloadFileServer(client)
        if receive_info == 'cancel':
            self.deleteFileServer(client)

    def beginInterface(self):
        while True:
            client, address = self.server_socket.accept()
            choice = client.recv(1024).decode()
            print(choice)
            t = threading.Thread(target=self.receiveState, args=(client, choice))
            t.start()


    # 调整文件大小的表达
    def modifySizeName(self, object_path):
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
    # 调整修改时间
    def timeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    def transPath(self, path):
        if path.find('\\') != -1:
            path_list = path.split('\\')
            new_path = path_list[0]
            for index in range(1, len(path_list)):
                new_path += (os.sep + path_list[index])
        else:
            path_list = path.split('/')
            new_path = path_list[0]
            for index in range(1, len(path_list)):
                new_path = os.sep + path_list[index]

        return new_path

if __name__ == '__main__':
    server_start = Server()
    print('begin connecting...')
    server_start.beginInterface()



    # def uploadServer(self, client):
    #     #while True:
    #     path = client.recv(1024).decode()
    #     filename_index = path.rfind(os.sep)
    #     filename = path[filename_index, ]
    #     part_list = filename.split(os.sep)
    #
    #     with open(filename, 'ab') as f:
    #         data = client.recv(1024)
    #         f.write(data)
    #     f.close()
    #
    # def creatDir(self, path):
    #     folders = []
    #     while not os.path.isdir(path) and path != '':
    #         path, suffix = os.path.split(path)
    #         folders.append(suffix)
    #
    #     for folder in folders[::-1]:
    #         path = os.path.join(path, folder)
    #         os.mkdir(path)
    #
    #



    # def uploadServerThreadPool(self, client):
    #     pool = threadpool.ThreadPool(10)
    #     requests = threadpool.makeRequests(self.uploadServer, client)
    #     [pool.putRequest(req) for req in requests]
    #     pool.wait()



