# ~*~ coding: utf-8 ~*~
"""
@Author: 陈乐
@Ide: Pycharm
@Time:
@Note:
@Project: 
"""

import _thread
import os
import Local.Client

class Upload:
    def __init__(self):
        pass

    def uploadDir(self, dir_name):
        self.origin_dir_name = dir_name
        self.recursionUpload(dir_name)

    def recursionUpload(self, dir_name):

        upload_client = Local.Client.Client()

        object_list = os.listdir(dir_name)  # 得到文件夹下的所有文件名称
        for item in object_list:
            object_path = os.path.join(dir_name, item)
            if os.path.isdir(object_path):
                self.recursionUpload(object_path)
            else:
                # 第一个参数是文件路径，　第二个参数是原始的上传文件夹
                upload_client.uploadFileClient(object_path, self.origin_dir_name)
                # print(object_path + '\t' + self.origin_dir_name)


if __name__ == '__main__':
    Upload().uploadDir('d:\\')












