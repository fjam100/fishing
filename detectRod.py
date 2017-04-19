import cv2
import numpy as np

# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im
 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in xrange(ramp_frames):
 temp = get_image()
print("Taking image...")
# Take the actual image we want to keep

for i in range(1):
    #img = get_image()
    img = cv2.imread('rodRed2.jpg')

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #60-100-100
    #55 82 84
    lower_red = np.array([0,180,180])
    upper_red = np.array([15,240,240])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    """
    cv2.imshow('img',img)
    cv2.imshow('mask',mask)"""
    #cv2.imshow('res',res)
    #cv2.waitKey(1)
    cv2.imwrite('1thresh.jpg',res)


    #blur = cv2.blur(res,(5,5))
    median = cv2.medianBlur(res,9)
    #cv2.imwrite('blur.jpg',blur)
    cv2.imwrite('1median.jpg',median)


    img = median.copy()
    gray = cv2.cvtColor(median,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    cv2.imwrite('1canny.jpg',edges)
    cv2.imshow('res2',edges)
    #cv2.waitKey(1)

    lines = cv2.HoughLines(edges,1,np.pi/180,200)
   
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow('1houghlines3',img)
    cv2.imwrite('1line.jpg',img)

