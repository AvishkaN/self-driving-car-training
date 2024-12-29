import numpy as np
import os
import cv2

import json

with open("labelConfig.json", "r") as json_file:
    labelConfig = json.load(json_file)
    print(labelConfig['current_folder_path'])


# Define the directory name
folder_name = labelConfig['current_folder_path']
saveNpArray = f'{folder_name}/allImages'
saveNpArrayTarget = f'{folder_name}/allImages_targets'

# Initialize lists to hold the reconstructed data
reconstructed_images = []
reconstructed_targets = []

# Iterate through saved chunks
chunk_index = 0
while True:
    image_file = f"{saveNpArray}_chunk_{chunk_index}.npz"
    target_file = f"{saveNpArrayTarget}_chunk_{chunk_index}.npz"
    
    # Check if the files exist
    if not os.path.exists(image_file) or not os.path.exists(target_file):
        break  # Stop when no more chunks are found
    
    # Load the chunk
    with np.load(image_file) as image_data:
        reconstructed_images.append(image_data['image_chunk'])
    with np.load(target_file) as target_data:
        reconstructed_targets.append(target_data['target_chunk'])
    
    chunk_index += 1

# Combine all chunks into single arrays
reconstructed_images = np.concatenate(reconstructed_images, axis=0)
reconstructed_targets = np.concatenate(reconstructed_targets, axis=0)

# Verify the shapes
print(f"Reconstructed images shape: {reconstructed_images.shape}")
print(f"Reconstructed targets shape: {reconstructed_targets.shape}")


# allImages=reconstructed_images[::-1]
# allImagesTarget=reconstructed_targets[::-1]
allImages=reconstructed_images
allImagesTarget=reconstructed_targets


print(allImages.shape)

for i, imageData in enumerate(allImages):
        # "2-data-3-W.png".split('-')[-1].split('.')[0]
        if(allImagesTarget[i] == 'A' or allImagesTarget[i] == 'D' or allImagesTarget[i] == 'W'):
            fileName=f"{folder_name}/{folder_name}-{i+1}-{allImagesTarget[i]}.png"
            print(fileName)

            # imageData=cv2.resize(imageData,(224,224))
            

            # Get the original dimensions
            original_height, original_width = imageData.shape[:2]

            # Calculate the new height (50% of the original height)
            # new_height = original_height // 2

            # # Crop the image to the bottom half
            # # cropped_image = imageData[:new_height, :]
            # cropped_image = imageData[new_height:, :]


            # Calculate the starting point for the bottom 60% (remaining 40% is cropped)
            start_height = int(original_height * 0.45)
            # start_height = int(original_height * 0)

            # Crop the image to the bottom 60%
            cropped_image = imageData[start_height:, :]

            
            # print(fileName)
            cv2.imwrite(fileName, cropped_image)
