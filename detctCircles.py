import cv2
import numpy as np;
import functionsFile as fn
 
# Read image
image = cv2.imread("fish.jpg", cv2.IMREAD_GRAYSCALE)
output = image.copy()

# detect circles in the image
circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, 1, minRadius=100, maxRadius=250)
 
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
	# show the output image
	cv2.imshow("output", np.hstack([image, output]))
	cv2.waitKey(0)
