from PIL import Image, ImageGrab
from functools import partial
import pyautogui
import pygetwindow
import pytesseract
import numpy as np
import cv2

'''ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
screen = pyautogui.screenshot()
screen.save("test.png")
img_cv = np.array(screen)'''

filename = "/home/pele/Téléchargements/image.png"

img = cv2.imread(filename)
height, width, _channel = img.shape


img_crop = img[0:int(height/8), 0:int(width/8)]
img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
# binarize with threshold and invert image
_, img_bin = cv2.threshold(img_crop, 60, 255, cv2.THRESH_BINARY_INV)

text = pytesseract.image_to_string(img_bin)

print(text)