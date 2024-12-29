import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from directkeys import ReleaseKey, PressKey, W, A, S, D
from getkeys import key_check
import os
from grabscreen import grab_screen
import json
t_time = 0.09

dataList=[]

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    #ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)
    



def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    output = [0,0,0]
    
    if 'A' in keys:
        # output[0] = 1
        output[0] = 'A'
    elif 'D' in keys:
        output[2] = 'D'
    else:
        output[1] = 'Else'
    return output



def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img,lines):
    try:
        for line in lines:
            coords=line[0]
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[0,255,0],3)
    except:
        pass


def process_img(original_image):
    # processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(original_image, threshold1=240, threshold2=300)
    verticies=np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500]])
    processed_img=roi(processed_img,[verticies])
    roi_image=processed_img
    processed_img=cv2.GaussianBlur(processed_img,(3,3),0)
    # processed_img=cv2. cvtColor(processed_img, cv2. COLOR_BGR2RGB)
    lines=cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),150,5)
    draw_lines(original_image,lines)
    # return processed_img
    return original_image,roi_image

for i in list(range(2))[::-1]:
    print(i + 1)
    time.sleep(1)

last_time = time.time()
while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
    # screen=cv2. cvtColor(screen, cv2. COLOR_BGR2RGB)

    new_screen,roi_image=process_img(screen)
    keys = key_check()
    output = keys_to_output(keys)
    print(output)
    dataList.append(output)

    straight()
    left()



    # training_data.append([screen,output])


    # PressKw

    print(screen.shape)
    # cv2.imwrite("image_name.jpg", screen)


    # printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8')
    print('Loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    # cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    cv2.imshow('window1', cv2.cvtColor(new_screen, cv2.COLOR_BGR2RGB))
    cv2.imshow('window2', cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print('q pressed')


        # Define the file name to save the JSON
        file_name = "data.json"

        # Write the array to the JSON file
        with open(file_name, "w") as json_file:
            json.dump(dataList, json_file, indent=4)

        print(f"Array has been written to {file_name}")

        cv2.destroyAllWindows()
        break