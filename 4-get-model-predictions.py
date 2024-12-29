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
t_time = 0.000009
import win32api
import time
import os
import tensorflow as tf
import json



with open("labelConfig.json", "r") as json_file:
    labelConfig = json.load(json_file)
    print(labelConfig)
    print(labelConfig['labels']['A'])

loaded_model = tf.keras.models.load_model("model2.h5")

# Map virtual key codes to their names
key_mapping = {
    "A": 0x41,
    "S": 0x53,
    "D": 0x44,
    "W": 0x57
}


IMG_SIZE = 224 
# Data Preparation
def preprocess_images(X):
    # Resize and normalize images
    X_resized = tf.image.resize(X, [IMG_SIZE, IMG_SIZE])
    return tf.keras.applications.mobilenet_v2.preprocess_input(X_resized)

i=0

t_time = 0.09

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

# def left():
#     PressKey(W)
#     PressKey(A)

#     ReleaseKey(W)
#     ReleaseKey(D)
#     #ReleaseKey(A)
#     time.sleep(t_time)
#     ReleaseKey(A)

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
print(len(os.listdir('all-data')))

while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 0, 800, 600)))
    # screen_ori=screen.copy()

    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    screenBGR = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    
    print(screen.shape)

    # testImg=cv2.imread(img_path)
    # print(testImg.shape)
    # prepossedImg=preprocess_images(screen)
    # predictedImg=loaded_model.predict(np.expand_dims(prepossedImg,axis=0))
    # print(predictedImg[0][0])
    # predictedStr=(str(int(predictedImg[0][0])))
    # print(predictedStr)

    testImg = screen
    preprocessedImg = preprocess_images(testImg)
    predictedImg = loaded_model.predict(np.expand_dims(preprocessedImg, axis=0))
    predicted_class = np.argmax(predictedImg, axis=1)[0]
    lastPrediction = labelConfig['labels_reversed'][str(predicted_class)]


    # break
    # lastPrediction=d['labels_reversed'][predictedStr]
    print(predictedImg)
    # print(predicted_class)
    # print(lastPrediction)


   
    # left()
    # right()

    # if(lastPrediction=="A"):
    #     left()
    # elif(lastPrediction=="D"):
    #     right()

    # if(lastPrediction=="W"):
    #     straight()
    # elif(lastPrediction=="A"):
    #     right()
    # elif(lastPrediction=="D"):
    #     left()
    # elif(lastPrediction=="S"):
    #     reverse()

    # straight()
    # left()
    # right()
    # reverse()

    last_time = time.time()
    cv2.imshow('window1', screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

