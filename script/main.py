from socket import timeout
import time
import torch
import cv2
import numpy as np
from mss import mss
import keyboard
import serial


model = torch.hub.load(r'mouse_driver\script\yolov5','custom', path=r'mouse_driver\script\best.pt', source='local')
arduino = serial.Serial("com4", "115200", timeout = .1)

def SendCoordinate(code):
    code = str(code)
    arduino.write(str.encode(code))

def CalculationDistance(x,y): #distance : (100, -100) -> " n,100,p,100* " in arduino
    if x < 0:
        x *=-1
        x_d = "n"
    else:
        x_d = "p"
    if y<0:
        y *=-1
        y_d = "n"
    else:
        y_d = "p"
        
    x_v = int(x/5)
    y_v = int(y/5)
    code = x_d + "," + str(x_v) + "," + y_d + "," + str(y_v) + "*"
    #print the code
    return code

with mss() as sct:
    monitor = {"top": 220, "left": 640, "width":640, "height": 640}
    
    while(True):
        screenshot = np.array(sct.grab(monitor))
        result = model(screenshot, size=640)
        df=result.pandas().xyxy[0]
        
        try:
            xmin = int(df.iloc[0,0])
            ymin = int(df.iloc[0,1])
            xmax = int(df.iloc[0,2])
            ymax = int(df.iloc[0,3])
            
            HeadLevel = (int(xmin + (xmax-xmin) /2 ), int(ymin + (ymax-ymin) / 8 ))
            cv2.circle(screenshot, HeadLevel, 4, (0,255,0), thickness = -1)
            cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255,0,0), 2)
            
            distance = (HeadLevel[0] - 320 , HeadLevel[1] -320)
            
            if keyboard.is_pressed("f"):
                code = CalculationDistance(int(distance[0]), int(distance[1]))
                SendCoordinate(code)
                time.sleep(0.175)
            
        except:
            print("", end="")
        
        cv2.imshow("frame", screenshot)
        if(cv2.waitKey(1)==ord('q')):
            cv2.destroyAllWindows()
            break
        
