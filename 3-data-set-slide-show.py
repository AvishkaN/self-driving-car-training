import cv2
import os

import json

with open("labelConfig.json", "r") as json_file:
    labelConfig = json.load(json_file)
    print(labelConfig['current_folder_path'])


# Define the directory name
image_folder = labelConfig['current_folder_path']



# Get all image file paths from the folder
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))])

print(image_files)




text = "Hello, OpenCV!"
org = (50, 100)  # Bottom-left corner of the text
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 0, 0)  # Blue color
thickness = 2

# Check if images exist
if not image_files:
    print("No images found in the folder!")
    exit()

# Load the first image to get frame dimensions
frame = cv2.imread(os.path.join(image_folder, image_files[0]))
height, width, _ = frame.shape

# Loop through the images and display them
for image_file in image_files:
    print(image_file.split('-')[1].split('.')[0])
    # print(image_file.split('-')[1])
    # text=image_file.split('-')[1].split('.')[0]
    text=image_file.split('-')[-1].split('.')[0]
    frame = cv2.imread(os.path.join(image_folder, image_file))

    cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow('data gathering', frame)

    # Delay to simulate frame rate (e.g., 30 frames per second)
    cv2.waitKey(5)  # 33ms ~ 30 FPS (1000ms / 30)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
