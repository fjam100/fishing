import cv2
import numpy as np;
import math

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

openposns=[]
for i in range(300):
    camera_capture = get_image()
    im= cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)
        
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
del(camera)

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
        temp.append(i)
        temp.append(closestind)
       while closest<2 and closestind<len(openposns)-2:
            closest,closestind=findClosest(closestind,openposns)
            temp.append(closestind)
       if temp!=[]:
            linked.append(temp)
       
print linked

print linked[0][0]

"""
for i in linked:
    for j in i:
        """
