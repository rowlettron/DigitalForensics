import os.path
import time

print('File         :', __file__)
print('Access time  :', time.ctime(os.path.getatime(__file__)))
print('Modified time:', time.ctime(os.path.getmtime(__file__)))
print('Change time  :', time.ctime(os.path.getctime(__file__)))
print('Size         :', os.path.getsize(__file__))

testfile = '/Users/ron/Documents/GitHub/DigitalForensics/results.txt'

print('File         :', testfile)
print('Access time  :', time.ctime(os.path.getatime(testfile)))
print('Modified time:', time.ctime(os.path.getmtime(testfile)))
print('Change time  :', time.ctime(os.path.getctime(testfile)))
print('Size         :', os.path.getsize(testfile))

