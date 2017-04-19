import cv2
import numpy as np
import copy

def detectRod(img):
    
    #img = cv2.imread('rod3.jpg')
    back=copy.copy(img)
    #cv2.imshow('in',img)
    #cv2.waitKey()

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #60-100-100
    #55 82 84
    lower_blue = np.array([0,180,180])
    upper_blue = np.array([20,240,240])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    """
    cv2.imshow('img',img)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)"""
    cv2.imwrite('cThresh.jpg',res)
    #cv2.waitKey()

    #blur = cv2.blur(res,(5,5))
    median = cv2.medianBlur(res,7)
    #cv2.imwrite('blur.jpg',blur)
    cv2.imwrite('cmedian.jpg',median)


    img = res.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    cv2.imwrite('canny.jpg',edges)
    
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    if lines is not None:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        print('detected')
        cv2.imwrite('choughlines3.jpg',img)
        return img
    return back
