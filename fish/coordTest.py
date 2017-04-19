import pygame
import sys
import time
import serial
import math
import cv2
import csv
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(cv2.cv.CV_CAP_PROP_FPS, 60)

while 1:
    ret, frame = camera.read()

    image=frame
    cv2.imshow('fish', frame)
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)

    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 50)
 
    # ensure at least some circles were found
    if circles is not None:
	    # convert the (x, y) coordinates and radius of the circles to integers
	    circles = np.round(circles[0, :]).astype("int")
     
	    # loop over the (x, y) coordinates and radius of the circles
	   

	    for (xcoord, ycoord, r) in circles:
		    # draw the circle in the output image, then draw a rectangle
		    # corresponding to the center of the circle
		    cv2.circle(output, (xcoord, ycoord), r, (0, 255, 0), 4)
		    print "x: ", xcoord;
		    print ycoord;
		    #writer.writerow([xcoord,ycoord, x, pan, tilt]);
		    cv2.rectangle(output, (xcoord - 5, ycoord - 5), (xcoord + 5, ycoord + 5), (0, 128, 255), -1)
     
	    # show the output image
	    cv2.imshow("output", np.hstack([image, output]))
	    cv2.waitKey(1)
    
