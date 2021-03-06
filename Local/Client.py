# 1、并行上传下载
# 2、断点续传，断点下载
# 3、密码注册登录
# 4、服务器信息时事更新

import socket
import time
import configparser
import os

BUFF = 1024

class Client:
    def __init__(self):
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        address = (ip, port)
        self.client_socket.connect(address)
        self.load_process = 0

        self.stop_button = False
        self.cancel_button = False

        self.remote_file_size = 0

    def checkForConnecting(self):
        pass

    # 上传登录信息
    def checkForUserAndPassword(self, username, password):
        message = 'check_for_username_and_password'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'begin_check_for_username_and_password':
                print('开始检查用户名密码')
                self.client_socket.send(username.encode())
                self.client_socket.send(password.encode())
                message = self.client_socket.recv(1024).decode()
                if message == 'username_and_password_are_ok':
                    return True
                else:
                    return False
            else:
                return False
        except socket.error:
            return False

    # 上传注册信息
    def registerSocket(self,address, username, password):
        message = 'connecting'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'connect_ok':
                print('连接已建立')
                self.client_socket.send(username.encode())
                self.client_socket.send(password.encode())
            return False
        except socket.error:
            return True

    # 获取文件的路径结构
    def getFilePathStruct(self, up_path, dir_len , dir_info, file_info):
        DIR = '0'
        FILE = '1'
        message = 'ask_for_file'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'connect_ok':
                print('连接已建立')
                self.client_socket.send(up_path.encode())
                len_of_list = int(self.client_socket.recv(1024).decode())
                dir_len = len_of_list

                for i in range(len_of_list):
                    file_or_dir = self.client_socket.recv(1024).decode()

                    if file_or_dir == DIR:
                        dir_name = self.client_socket.recv(1024).decode()
                        change_time = self.client_socket.recv(1024).decode()
                        dir_info.append([dir_name, change_time])
                    elif file_or_dir == FILE:
                        dir_name = self.client_socket.recv(1024).decode()
                        file_size = self.client_socket.recv(1024).decode()
                        change_time = self.client_socket.recv(1024).decode()
                        file_info.append([dir_name, file_size, change_time])


        except socket.error:
            return True

        self.client_socket.close()

    def getFilesList(self, dir, info_list):
        message = 'get_files_list'
        self.client_socket.send(message.encode())
        time.sleep(0.001)
        self.client_socket.send(dir.encode())
        length = self.client_socket.recv(1024).decode()
        for i in range(int(length)):
            type = self.client_socket.recv(1024).decode()
            # 文件
            if type == '0':
                # 相对文件名
                name = self.client_socket.recv(1024).decode()
                info_list.append(['0',name])
            else:
                name = self.client_socket.recv(1024).decode()
                info_list.append(['1', name])

    # 下载文件到指定目录下
    def download(self, relative_file_path, save_path):
        message = 'download'
        self.client_socket.send(message.encode())
        time.sleep(0.002)
        print(relative_file_path)
        self.client_socket.send(relative_file_path.encode())

        while True:
            # 文件保存路径
            file_path = save_path + '/' + relative_file_path
            up_path = file_path[:file_path.rfind('/')]

            if not os.path.isdir(up_path):
                os.makedirs(up_path)

            # 文件大小
            file_size_str = self.client_socket.recv(1024).decode()
            file_size = int(file_size_str)
            self.setRemoteFileSize(file_size)       # 生成可视化文件路径
            old_time = time.time()
            while True:
                new_time = time.time()
                # 暂停按钮
                while self.stop_button:
                    time.sleep(1)
                # 取消按钮
                if self.cancel_button:
                    time.sleep(0.1)
                    self.client_socket.send('cancel'.encode())
                    os.remove(file_path)
                    break
                # 进度统计
                if new_time - old_time > 0.1:
                    process = round(os.path.getsize(file_path) / file_size * 100)
                    self.setLoadProcess(process)
                    old_time = new_time
                # 下载到本地
                data = self.client_socket.recv(1024)
                if not data:
                    break
                else:
                    try:
                        with open(file_path, 'ab') as f:
                            f.write(data)
                    except IOError as err:
                        print("File Error:" + str(err))

            self.setLoadProcess(100)
            self.client_socket.close()
            return


    # 上传文件到当前的文件夹之下, filename是文件名, file_path是本地的文件路径
    def upload(self, up_path, filename, file_path):
        self.client_socket.send('upload'.encode())
        time.sleep(0.2)
        self.client_socket.send(up_path.encode())
        time.sleep(0.2)
        self.client_socket.send(filename.encode())
        time.sleep(0.2)
        total_line = 0
        try:
            with open(file_path, 'rb') as f:
                for line in f:
                    total_line += 1
            f.close()
            i = 0
            with open(file_path, 'rb') as f:
                for line in f:
                    # 暂停按钮
                    while self.stop_button:
                        time.sleep(1)
                        if self.cancel_button:
                            break
                    # 取消按钮
                    if self.cancel_button:
                        break

                    self.client_socket.send(line)
                    i += 1
                    count = round(i/total_line*100)
                    self.setLoadProcess(count)
        except IOError as err:
            print("File Error:" + str(err))


    def setLoadProcess(self, load_process):
        self.load_process = load_process
    def getLoadProcess(self):
        return self.load_process

    def setStopButton(self, stop_button):
        self.stop_button = stop_button
    def getStopButton(self):
        return self.stop_button

    def setCancelButton(self, cancel_button):
        self.cancel_button = cancel_button
    def getCancelButton(self):
        return self.cancel_button

    def setRemoteFileSize(self, size):
        self.remote_file_size = size
    def getRemoteFileSize(self):
        return self.remote_file_size

    def SignUp(self):
        pass

    def deleteDirClient(self, dir):
        message = 'delete_dir'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'connect_ok':
                print('连接已建立')
                self.client_socket.send(dir.encode())
            return True
        except socket.error:
            return False

    def deleteFileClient(self, file):
        message = 'delete_file'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'connect_ok':
                print('连接已建立')
                self.client_socket.send(file.encode())
            return True
        except socket.error:
            return False

    def getRootPathClient(self):
        message = 'root_path'
        try:
            self.client_socket.send(message.encode())
            receive_message = self.client_socket.recv(1024).decode()
            if receive_message == 'connect_ok':
                print('连接已建立')
                root_path = self.client_socket.recv(1024).decode()
                return root_path
            return 'error'
        except socket.error:
            return 'error'
    def heartBeat(self):
        message = 'heart_beat'
        self.client_socket.sendall(message.encode())
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'udp_port'))
        address = (ip, port)
        udp_socket.connect(address)
        while True:
            udp_socket.send('1'.encode())
            time.sleep(0.3)


if __name__ == '__main__':
    pass