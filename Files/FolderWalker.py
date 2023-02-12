import os
import os.path
import time

os.chdir('/Users/ron/Documents/GitHub/HurricaneStats')

for (root,dirs,files) in os.walk('.', topdown=True):
    # print(root)
    # print(dirs)
    # print(files)
    # print(os.path.abspath(root))
    for file in files:
        filename = os.path.abspath(root) + '/' + file 
        print(filename)
        print('File         :', file)
        print('Access time  :', time.ctime(os.path.getatime(filename)))
        print('Modified time:', time.ctime(os.path.getmtime(filename)))
        print('Change time  :', time.ctime(os.path.getctime(filename)))
        print('Size         :', os.path.getsize(filename))
    print('**************************************************************************')

