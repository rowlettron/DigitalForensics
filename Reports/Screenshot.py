import numpy as np
import matplotlib.pyplot as plt
import pyscreenshot as ImageGrab
image = ImageGrab.grab()
plt.imshow(image, cmap='gray', interpolation='bilinear')
plt.show()  

 