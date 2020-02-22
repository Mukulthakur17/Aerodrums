import threading

import cv2
import numpy as np
from playsound import playsound

cap = cv2.VideoCapture(0)
Y_hit = 0
B_hit = 0

def Playsound(instr):
    if instr == 1:
        playsound('DrumSnare.wav')
    elif instr == 2:
        playsound('DrumHeavySnare.wav')
    elif instr == 3:
        playsound('DrumNoiseClap.wav')
    elif instr == 4:
        playsound('DrumCymbal.wav')
    elif instr == 5:
        playsound('DrumHiHat.wav')


#Color to be Detected:
Lb1 = np.array([140, 70, 200])  #Pink
Ub1 = np.array([185, 120, 255]) #Pink

Lb2 = np.array([14, 49, 100])  #Yellow
Ub2 = np.array([30, 139, 255]) #yellow


def for_color(Lb, Ub, hit):
    #Filters:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_C = cv2.inRange(hsv, Lb, Ub)
    #mask_C = cv2.bitwise_or(mask_R, mask_B)
    blur = cv2.GaussianBlur(mask_C, (5,5), 0)
    _, thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)

    #Closing Filter:
    kernal = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernal)

    #Contour Formation:
    contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours :
        if cv2.contourArea(contour) < 1500:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
        cv2.circle(frame, (int(x + w/2), int(y + h/2)), 15, (0, 0, 255), -1)

        #Sounds:
        if 150 <= (x + w/2) <= 290 and 470 <= (y + h/2) <= 610:
            if hit == 1:
                continue
            else:
                threading._start_new_thread(Playsound, (1,))
                hit = 1
        elif 410 <= (x + w/2) <= 550 and 470 <= (y + h/2) <= 610:
            if hit == 2:
                continue
            else:
                threading._start_new_thread(Playsound, (2,))
                hit = 2
        elif 670 <= (x + w/2) <= 810 and 470 <= (y + h/2) <= 610:
            if hit == 3:
                continue
            else:
                threading._start_new_thread(Playsound, (3,))
                hit = 3
        elif 230 <= (x + w/2) <= 370 and 230 <= (y + h/2) <= 360:
            if hit == 4:
                continue
            else:
                threading._start_new_thread(Playsound, (4,))
                hit = 4
        elif 580 <= (x + w/2) <= 720 and 230 <= (y + h/2) <= 360:
            if hit == 5:
                continue
            else:
                threading._start_new_thread(Playsound, (5,))
                hit = 5
        else :
            hit = 69

    return hit


while cap.isOpened :

    #Flip & Resize:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (960, 720))
    
    B_hit = for_color(Lb1, Ub1, B_hit)  #Blue
    Y_hit = for_color(Lb2, Ub2, Y_hit)  #Yellow
        
    #Frame:
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, 'Air Drums', (220, 100), font, 3, (0, 0, 255), 6, cv2.LINE_AA)
    cv2.line(frame, (200, 110), (760, 110), (0, 0, 0), 2)
    cv2.rectangle(frame, (150, 470), (290, 610), (0, 255, 0), 3)  #Drum 1
    cv2.rectangle(frame, (410, 470), (550, 610), (0, 255, 0), 3)    #2
    cv2.rectangle(frame, (670, 470), (810, 610), (0, 255, 0), 3)   #3
    cv2.rectangle(frame, (230, 230), (370 ,360), (255, 0, 0), 3)  #Chann 4
    cv2.rectangle(frame, (580, 230), (720, 360), (255, 0, 0), 3)    #5


    cv2.imshow('Air Drums', frame)
    if cv2.waitKey(60) == 27:
        break

cap.release()
cv2.destroyAllWindows()