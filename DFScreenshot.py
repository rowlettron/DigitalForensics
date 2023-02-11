import pyscreenshot as ImageGrab
import numpy as np
import matplotlib.pyplot as plt

image = ImageGrab.grab()

plt.imshow(image, cmap='gray', interpolation='bilinear')
plt.show()

image.save('image123.png')