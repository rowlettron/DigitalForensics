#-- include('examples/showgrabbox.py')--#
import pyscreenshot as ImageGrab

if __name__ == '__main__':
    # part of the screen
    im = ImageGrab.grab(bbox=(0, 0, 810, 810)) # X1,Y1,X2,Y2
    im.show()