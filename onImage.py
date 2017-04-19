import cv2
import numpy as np;
import functionsFile as fn
 
# Read image
im = cv2.imread("test_image4.png", cv2.IMREAD_GRAYSCALE)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
#im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

openposns=[]
keypoints2=[]
for i in keypoints:
   #print i.size
   if i.size>3:
        keypoints2.append(i)
        openposns.append(i.pt)
im_with_keypoints = cv2.drawKeypoints(im, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(1)

linked=[]
for i in range(0,len(openposns)-2):
       flag=0
       for j in linked:
            if i in j:
                flag=1
       if flag == 1:
            continue
       temp=[]
       closest,closestind=fn.findClosest(i,openposns)
       #print closest
       if closest<25:
        temp.append(i)
        temp.append(closestind)
       
       while closest<25 and closestind<len(openposns)-2:
            closest,closestind=fn.findClosest(closestind,openposns)
            temp.append(closestind)
       if temp!=[]:
            linked.append(temp)
            
print linked 
       
dispoint=[]
for i in linked[1]:
    #print keypoints2[i].pt
    if i>0:
        print keypoints2[i].pt[1]-keypoints2[i-1].pt[1]
    dispoint.append(keypoints2[i])

im_with_keypoints = cv2.drawKeypoints(im, dispoint, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey()

