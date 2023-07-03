from ctypes.wintypes import RGB
from PIL import ImageGrab
import cv2
import numpy as np
import keyboard
import time


x = 0
def TakeScreenshot():
    screenshot = np.array(ImageGrab.grab(bbox=(640, 220, 1280, 860)))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    cv2.imwrite(file_name, screenshot)

while(True):
    try:
        if keyboard.is_pressed('u'):
            file_name = str(x) + ".jpg"
            TakeScreenshot()
            x = x + 1
            time.sleep(1)
    except:
        print("ss failed")
