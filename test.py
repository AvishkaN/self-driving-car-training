import numpy as np
from PIL import ImageGrab
import cv2
import time
import win32api
import json
import os

# Load label configuration
with open("labelConfig.json", "r") as json_file:
    labelConfig = json.load(json_file)

# Key mappings and tracking
key_mapping = {"A": 0x41, "S": 0x53, "D": 0x44, "W": 0x57}
key_press_start_times = {}  # Tracks when a key was first pressed

# Angle calculation parameters
MAX_PRESS_DURATION = 2.0  # Maximum duration for full steering angle (2 seconds)
MAX_ANGLE = 45  # Maximum steering angle in degrees
current_angle = 0  # Current steering angle to display

def calculate_steering_angle(duration):
    """
    Map duration to steering angle.
    """
    duration = min(duration, MAX_PRESS_DURATION)  # Clamp duration
    return (duration / MAX_PRESS_DURATION) * MAX_ANGLE

def draw_steering_wheel_angle(img, angle):
    """
    Draw the steering wheel angle on an image.
    """
    height, width = img.shape[:2]
    center = (width // 2, height // 2)

    # Draw a circle for the wheel
    cv2.circle(img, center, 100, (0, 255, 0), 3)

    # Calculate the end point for the steering line
    angle_rad = np.deg2rad(angle - 90)  # Offset -90 to rotate correctly
    line_length = 100
    end_x = int(center[0] + line_length * np.cos(angle_rad))
    end_y = int(center[1] + line_length * np.sin(angle_rad))

    # Draw the steering line
    cv2.line(img, center, (end_x, end_y), (0, 255, 255), 3)

    # Display the angle as text
    cv2.putText(img, f"Angle: {angle:.2f} degrees", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

# Start countdown
for i in list(range(2))[::-1]:
    print(i + 1)
    time.sleep(1)

while True:
    # Capture the screen
    screen = np.array(ImageGrab.grab(bbox=(0, 0, 800, 600)))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    # Steering wheel display window
    steering_wheel_display = np.zeros((300, 300, 3), dtype=np.uint8)

    for key, vk_code in key_mapping.items():
        if win32api.GetAsyncKeyState(vk_code) & 0x8000:  # Key is pressed
            if key not in key_press_start_times:  # First press
                key_press_start_times[key] = time.time()
        else:  # Key is not pressed
            if key in key_press_start_times:  # Key was pressed before
                press_duration = time.time() - key_press_start_times[key]
                del key_press_start_times[key]  # Reset timer for this key

                if key in ["A", "D"]:  # Calculate angle for steering keys
                    current_angle = calculate_steering_angle(press_duration) * (-1 if key == "A" else 1)

    # Draw the current steering wheel angle
    draw_steering_wheel_angle(steering_wheel_display, current_angle)

    # Display the screens
    cv2.imshow("Game Capture", screen)
    cv2.imshow("Steering Wheel Angle", steering_wheel_display)

    # Quit if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
