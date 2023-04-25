from PIL import Image, ImageGrab
from functools import partial
import time
import pyautogui
import requests
import pygetwindow as gw
import pytesseract
import numpy as np
import cv2

username = "Thomas"

base_url = "http://gubendo.pythonanywhere.com/upload_height/"

print('LANCEZ BETON BRUTAL VITE VITE VITE')
time.sleep(20)

while True:
    time.sleep(10)
    
    screen = pyautogui.screenshot()
    img = np.array(screen)

    h, w, _channel = img.shape

    img_crop = img[0:int(h/8), 0:int(w/8)]
    img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_crop, 120, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(img_bin)

    height = text.split('M')[0]
    print(height)
    
    try:
        height_int = int(height)
    except:
        continue
    else:  
        data = {"user": username, "height": height_int}
        print(data)
        response = requests.post(base_url, json=data)
        print(response)
    