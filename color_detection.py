# Importing all modules
import cv2
import numpy as np
import serial
import time

#Serial object for communication with Arduino


arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
print(arduino)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
#while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value
 #Specifying upper and lower ranges of color to detect in hsv format
lower = np.array([15, 150, 20])
upper = np.array([35, 255, 255]) # (These ranges will detect Yellow)

# Capturing webcam footage
cap = cv2.VideoCapture(0)


ret = cap.set(3,640)
ret = cap.set(4,480)

while True:
    ret, video = cap.read() # Reading webcam footage

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

    mask = cv2.inRange(img, lower, upper) # Masking the image to find our color

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle

    cv2.imshow("mask image", mask) # Displaying mask image

    cv2.imshow("window", video) # Displaying webcam image

    cv2.waitKey(1)
