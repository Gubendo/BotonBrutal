from PIL import Image, ImageGrab
from functools import partial
import time
import pyautogui
import requests
#import pygetwindow
import pytesseract
import numpy as np
import cv2

username = "Thomas"
monitor = 2


base_url = "http://gubendo.pythonanywhere.com/upload_height/"

'''ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
screen = pyautogui.screenshot()
screen.save("test.png")
img_cv = np.array(screen)'''


while True:
    time.sleep(10)
    filename = "/home/pele/Téléchargements/image.png" # TODO replace these lines by windows screenshot
    img = cv2.imread(filename)


    h, w, _channel = img.shape

    img_crop = img[0:int(h/8), 0:int(w/8)]
    img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_crop, 60, 255, cv2.THRESH_BINARY_INV)

    text = pytesseract.image_to_string(img_bin)

    height = text.split('M')[0]
    try:
        height_int = int(height)
    except:
        continue
    else:  
        data = {"user": username, "height": height_int}
        print(data)
        response = requests.post(base_url, json=data)
        print(response)