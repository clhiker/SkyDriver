import os
print(os.getcwd())
path = os.getcwd() + os.sep + 'page' + os.sep + 'home'
if not os.path.exists(path):
    os.makedirs(path)