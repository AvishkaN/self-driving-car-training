import numpy as np
import cv2



saveNpArray="data-2/allImages.npy"



allImages=np.load("data-2/allImages.npy")
allImagesTarget=np.load("data-2/allImages-targets.npy")


print(allImages[-1:])

for i, imageData in enumerate(allImages):
        
        fileName=f"data-2/{i+1}-{allImagesTarget[i]}.png"


        # Get the original dimensions
        original_height, original_width = imageData.shape[:2]

        # Calculate the new height (50% of the original height)
        # new_height = original_height // 2

        # # Crop the image to the bottom half
        # # cropped_image = imageData[:new_height, :]
        # cropped_image = imageData[new_height:, :]


        # Calculate the starting point for the bottom 60% (remaining 40% is cropped)
        start_height = int(original_height * 0.45)

        # Crop the image to the bottom 60%
        cropped_image = imageData[start_height:, :]

        
        # print(fileName)
        cv2.imwrite(fileName, cropped_image)
