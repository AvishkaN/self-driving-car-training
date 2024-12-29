import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from directkeys import ReleaseKey, PressKey, W, A, S, D
from getkeys import key_check
import os
# from grabscreen import grab_screen
import json
t_time = 0.09
import win32api
import time


import os


import json

with open("labelConfig.json", "r") as json_file:
    labelConfig = json.load(json_file)
    print(labelConfig['current_folder_path'])


# Define the directory name
folder_name = labelConfig['current_folder_path']

# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the directory
    os.mkdir(folder_name)
    print(f"The '{folder_name}' folder has been created.")
else:
    print(f"The '{folder_name}' folder already exists.")

# List of keys you want to monitor
keys_to_monitor = ["A", "S", "D", "W"]



# imageDataset=[]

# Map virtual key codes to their names
key_mapping = {
    "A": 0x41,
    "S": 0x53,
    "D": 0x44,
    "W": 0x57
}

dataList=[]
imageDataSet=[]
imageDataSetTargets=[]
i=0

# def straight():
# ##    if random.randrange(4) == 2:
# ##        ReleaseKey(W)
# ##    else:
#     PressKey(W)
#     ReleaseKey(A)
#     ReleaseKey(D)

# def left():
#     PressKey(W)
#     PressKey(A)
#     #ReleaseKey(W)
#     ReleaseKey(D)
#     #ReleaseKey(A)
#     time.sleep(t_time)
#     ReleaseKey(A)

# def right():
#     PressKey(W)
#     PressKey(D)
#     ReleaseKey(A)
#     #ReleaseKey(W)
#     #ReleaseKey(D)
#     time.sleep(t_time)
#     ReleaseKey(D)

t_time = 0.9

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
print(len(os.listdir('data')))

while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 0, 800, 600)))
    # screen_ori=screen.copy()

    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    screenBGR = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # new_screen,roi_image=process_img(screen)
    keys = key_check()
    output = keys_to_output(keys)
    print(screenBGR.shape)
    dataList.append(output)
    


    for key, vk_code in key_mapping.items():
        # Check if the key is pressed (state is negative)
        if win32api.GetAsyncKeyState(vk_code) & 0x8000:
            print(f"Key {key} is pressed")
            # if(key=='A' or key=='D'):
            imageDataSet.append(screen)
            imageDataSetTargets.append(key)
            i=i+1
            

    last_time = time.time()
    # cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    cv2.imshow('window1', screen)
    # cv2.imshow('window2', cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB))
    # print(0xFF)
    if cv2.waitKey(25) & 0xFF == ord('q'):


        # File paths for saving
        saveNpArray = f'{folder_name}/allImages'
        saveNpArrayTarget = f'{folder_name}/allImages_targets'

        # Chunk size for splitting the dataset
        chunk_size = 500

        # Save the dataset in chunks
        for i in range(0, len(imageDataSet), chunk_size):
            # Chunk data
            image_chunk = imageDataSet[i:i + chunk_size]
            target_chunk = imageDataSetTargets[i:i + chunk_size]
            
            # Save chunk with compression
            np.savez_compressed(f"{saveNpArray}_chunk_{i // chunk_size}.npz", image_chunk=image_chunk)
            np.savez_compressed(f"{saveNpArrayTarget}_chunk_{i // chunk_size}.npz", target_chunk=target_chunk)

        print(f"Dataset saved in chunks of size {chunk_size} to folder '{folder_name}'")

        cv2.destroyAllWindows()
        break

