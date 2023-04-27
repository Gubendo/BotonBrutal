from PIL import Image, ImageGrab
from functools import partial
import time
import pyautogui
import requests
import pytesseract
import numpy as np
import cv2

username = "Thomas"

base_url = "http://gubendo.pythonanywhere.com/upload_height/"


print('LANCEZ BETON BRUTAL VITE VITE VITE')
time.sleep(20)

base_conf = 0

while True:
    time.sleep(5)
    
    screen = pyautogui.screenshot()
    img = np.array(screen)

    h, w, _channel = img.shape

    img_crop = img[0:int(h/8), 0:int(w/8)]
    img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    img_inv = cv2.bitwise_not(img_crop)

    _, img_bin = cv2.threshold(img_crop, 120, 255, cv2.THRESH_BINARY)
    _, img_bin_inv = cv2.threshold(img_inv, 120, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_data(img_bin, output_type="data.frame")
    text = text[text.conf != -1]

    text_inv = pytesseract.image_to_data(img_bin_inv, output_type="data.frame")
    text_inv = text_inv[text_inv.conf != -1]

    if text.shape[0] == 1:
        row = text.iloc[0]
        if row["conf"] > 90:
            height = row["text"].split('M')[0]
            base_conf = row["conf"]
    
    if text_inv.shape[0] == 1:
        row = text_inv.iloc[0]
        if row["conf"] > 90 and row["conf"] > base_conf:
            height = row["text"].split('M')[0]

    try:
        height_int = int(height)
    except:
        continue
    else:  
        data = {"user": username, "height": height_int}
        print(data)
        response = requests.post(base_url, json=data)
        print(response)
    