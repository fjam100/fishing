import cv2
import numpy as np;
import math
#import detectRodFn

import sys
import time
import serial
import math
# import cv2

# camera = cv2.VideoCapture(0)
# camera.set(cv2.cv.CV_CAP_PROP_FPS, 60)

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=921600
)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def command(x, dx, pan, dpan, tilt, dtilt, home):
    x = clamp(int(x*65535), 0, 65534);
    xh = x >> 8 & 0xff
    xl = x & 0xff

    dx = clamp(int(dx*255), 0, 254)

    pan = clamp(int(pan*32767), -32767, 32767);
    panh = pan >> 8 & 0xff
    panl = pan & 0xff
    if panh < 0:
        panh = 255 - panh

    tilt = clamp(int(tilt*32767), -32767, 32767);
    tilth = tilt >> 8 & 0xff
    tiltl = tilt & 0xff
    if tilth < 0:
        tilth = 255 - tilth

    dpan = clamp(int(dpan/10.0*127), -127, 127)
    if dpan < 0:
        dpan = 255 + dpan
    dtilt = clamp(int(dtilt/10.0*127), -127, 127)
    if dtilt < 0:
        dtilt = 255 + dtilt

    flags = 0x00
    if home:
        flags = flags | 0x01

    checksum = (xh + xl + dx + panh + panl + tilth + tiltl + dtilt + dpan + flags) & 0x7f
    ser.write(bytearray([0xff, 0xff, dx, xh, xl, tilth, tiltl, panh, panl, dtilt, dpan, flags, checksum]))

import csv
with open('x.csv', 'rb') as f:
    reader = csv.reader(f)
    x_list = list(reader)

f.close()

with open('th.csv', 'rb') as f:
    reader = csv.reader(f)
    th_list = list(reader)

x = 0;
pan = -0.3
tilt = 0.8
tiltn = 0.8
tiltl = 0.7
tilth = 0.9

dt = 1/60.0
panlast = 0
tiltlast = 0
xlast = 0
dx = 0

command(0, 0, pan, 0, tilt, 0, True)

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
 
 
def euclideanDist(a,b):
    temp=0
    for i in range(len(a)):
        temp+=((a[i]-b[i])**2)
    return math.sqrt(temp)

def findClosest(i, array):
    if i==len(array)-1:
        print('Error in closest')
        return (0,i)
    closest=euclideanDist(array[i],array[i+1])
    closestind=i+1
    for j in (i+1,len(array)-1):
        if euclideanDist(openposns[i],openposns[j])<closest:
            closest=euclideanDist(openposns[i],openposns[j])
            closestind=j
            
    return  (closest,closestind)


# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in xrange(ramp_frames):
 temp = get_image()
print("Taking image...")
# Take the actual image we want to keep

openposns=[]
keypoints3=[]
count=0
index=[]

while True:
    for i in range(300):
        camera_capture = get_image()
        im= cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)
        imcopy=im
            
        # Set up the detector with default parameters.
        detector = cv2.SimpleBlobDetector()
         
        # Detect blobs.
        keypoints = detector.detect(im)
         
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        keypoints2=[]
        
        for i in keypoints:
            if i.size>20 and i.size<40:
                #print i.size
                keypoints2.append(i)
                keypoints3.append(i)
                index.append(count)
                count+=1
                openposns.append(i.pt)
        im_with_keypoints = cv2.drawKeypoints(im, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(1)
        file = "test_image"+str(i)+".png"
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!


    #cv2.imwrite(file, im_with_keypoints)
     
    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits


    #print openposns
    #print len(openposns)
    """
    a=[1,2]
    b=[1,1.5]
    c=[2,2.5]
    arr=[a,b,c]
    rann,ranm=findClosest(2,arr)
    print rann
    print ranm
    """
    linked=[]

    for i in range(0,len(openposns)-2):
           flag=0
           for j in linked:
                if i in j:
                    flag=1
           if flag == 1:
            continue
           temp=[]
           closest,closestind=findClosest(i,openposns)
           if closest<2:
            temp.append(keypoints3[i])
            temp.append(keypoints3[closestind])
           while closest<2 and closestind<len(openposns)-2:
                closest,closestind=findClosest(closestind,openposns)
                temp.append(keypoints3[closestind])
           if temp!=[]:
                linked.append(temp)
           
    #print linked

    displaypts=[]
    for i in linked:
        for j in i:
            displaypts.append(j)
    #print displaypts
    #im_display = cv2.drawKeypoints(im, displaypts, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # Show keypoints
    #cv2.imshow("Gathered", im_display)
    #cv2.waitKey(1)
            

    """
    keypoints3=[]
    for i in linked:
        for j in i:
            print keypoints3[j]"""
    #print linked[0][0]

    moveList = max(linked,key=len)
    #print moveList[len(moveList)/2]
    xindex=int(round(moveList[len(moveList)/2].pt[0]))
    yindex=int(round(moveList[len(moveList)/2].pt[1]))

    im_display2 = cv2.drawKeypoints(im, moveList, np.array([]), (255,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Get to", im_display2)
    cv2.waitKey(100)
    #cv2.destroyAllWindows()

    panlast = pan
    tiltlast = tilt
    xlast = x
    x=float(x_list[xindex][yindex])
    pan=float(th_list[xindex][yindex])

    factor = 1

    dtilt = (tilt - tiltlast)/dt
    dpan = (pan - panlast)/dt

    xdiff = abs(x - xlast)
    if xdiff > 0:
        dx = xdiff/dt * 0.45

    command(x, 0.2, pan, dpan, 0.8, dtilt, False)

    # ret, frame = camera.read()
    # cv2.imshow('fish', frame)
    # cv2.waitKey(1)
    time.sleep(1)
    dtilt=0.8
    count=0;
    while count<10:
        command(x, 0.2, pan, dpan, 0.6, dtilt, False)
        time.sleep(0.75)
        command(x, 0.2, pan, dpan, 0.9, dtilt, False)
        time.sleep(0.75)
        count+=1
