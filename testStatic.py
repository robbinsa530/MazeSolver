import sys
import math
import numpy as np
import cv2
import mazeSearch
from imaging import *

###########################
## Image Processing Library 
###########################

import argparse
#Parse cmd-line args and find/load image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])








 
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
#ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
#
#kernel = np.ones((1,1), np.uint8)	
#image = cv2.erode(image, kernel, iterations=1)
#
#findStartEnd(image) #TESTING
#
#cv2.imshow("image",image)
#
#size = np.size(image)
#skel = np.zeros(image.shape,np.uint8)
#
#element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#done = False
#
#while(not done):
#	eroded = cv2.erode(image,element)
#	temp = cv2.dilate(eroded,element)
#	temp = cv2.subtract(image,temp)
#	skel = cv2.bitwise_or(skel,temp)
#	image = eroded.copy()
#
#	zeros = size - cv2.countNonZero(image)
#	if zeros==size:
#		done = True
#	
#findStartEnd(skel) #TESTING
#	
#cv2.imshow("skel",skel)
#cv2.waitKey(0)
#
#exit()















##FAKE SLIDER VALS
contourThreshVal = 60
minBoundBoxVal = 5000
erosionVal = 40

#Do 10 times and get average
#total = 0
for i in range(1):
	thing = getMazeOutlineImage(image.copy(), contourThreshVal, minBoundBoxVal)
	if len(thing) < 3:
		print "oops, bye"
		exit()
	thresh,img,box = thing	
	
	dst2,h = getImageFromBox(thresh, box)

	#mazeImg,solvedImage,timez = getSolvedMaze(image.copy(), h, dst2, erosionVal)
	mazeImg,solvedImage = getSolvedMaze(image.copy(), h, dst2, erosionVal)

	#total += timez	

#print total / 10.0	
	
cv2.imshow("original", img)
#cv2.waitKey(0)	
cv2.imshow("solution", solvedImage)
#cv2.waitKey(0)	
cv2.imshow("solution2", mazeImg)
cv2.waitKey(0)	