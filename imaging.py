"""

imaging.py
----------

Alex Robbins, Andrew Hart
Intro to AI Section 1
Final Project (Maze Solver)


##############################
## Image Processing Library ## 
##############################

This file contains all the image processing functions used by the maze solver.
These include functions for:
	-finding start/end points of maze
	-finding the maze in a larger image
	-cropping the maze out of a larger image given its location
	-getting solution to the maze and drawing its solution on an image

"""

import sys
import math
import numpy as np
import cv2
import mazeSearch
from collections import OrderedDict

################################################################
"""
Finds start point and end point by scanning list of found path-lines looking
 for lines with endpoints closest to the edge of the image

params:
	mazeImg: A cropped, thresholded, eroded image of the maze
	
returns:
	(start,end): start/end points of maze each in (x,y) format	
"""
################################################################
def findStartEnd(mazeImg):
	#Find paths
	edges = cv2.Canny(cv2.bitwise_not(mazeImg),100,200,apertureSize = 3)
	minLineLength = 25
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges,1,np.pi/180,25,minLineLength,maxLineGap)
	
	#mazeImg2 = cv2.cvtColor(mazeImg, cv2.COLOR_GRAY2BGR)
	
	horiz = {}
	vert = {}
	if lines is not None:
		#print lines
		for x in lines:
			for x1,y1,x2,y2 in x:
				#Assume that each line will either be roughly vertical or roughly horizontal
				#Group horizontal lines by their y value, and vertical lines by their x value
				if (abs(y2-y1) <= 2):
					key = int((y1+y2)/2)
					if key in horiz:
						horiz[key].append(x)
					else:	
						horiz[key] = [x]
				else:
					key = int((x1+x2)/2)
					if key in vert:
						vert[key].append(x)
					else:	
						vert[key] = [x]
	
	#Sort dictionaries by keys
	horiz = OrderedDict(sorted(horiz.items()))
	vert = OrderedDict(sorted(vert.items()))
	
	#Combine lines that are close to be single lines. Put them in this new dictionary
	horizCompressed = {}
	vertCompressed = {}
	
	#Go through list of horizontal lines and combine lines at similar y values into a single line
	#Go through list of vertical lines and combine lines at similar x values into a single line
	#This puts all lines as close to the center of the paths as possible
	first = True
	currKey = -9
	tempList = []
	for key in horiz:
		if key > currKey + 8:
			if first:
				first = False
				currKey = key
			else:	
				horizCompressed[currKey + 4] = tempList	
				tempList = []				
				currKey = key
				
		for line in horiz[key]:
			#line = x1,y1,x2,y2
			line[0,1] = currKey + 4	#y1
			line[0,3] = currKey + 4	#y2	
			tempList.append(line)	
	
	if not not tempList:
		horizCompressed[currKey + 4] = tempList	
	
	first = True
	currKey = -9
	tempList = []
	
	for key in vert:
		if key > currKey + 8:
			if first:
				first = False
				currKey = key
			else:	
				vertCompressed[currKey + 4] = tempList		
				tempList = []				
				currKey = key

		for line in vert[key]:
			#line = x1,y1,x2,y2
			line[0,0] = currKey + 4	#x1
			line[0,2] = currKey + 4	#x2
			tempList.append(line)			
	
	if not not tempList:
		vertCompressed[currKey + 4] = tempList	
	
	###TEST! DRAW LINES!
	#for key in horizCompressed:
	#	for ln in horizCompressed[key]:
	#		for x1,y1,x2,y2 in ln:
	#			cv2.line(mazeImg2,(x1,y1),(x2,y2),(255,0,0),2)	#Draw horizontal lines Blue
	#
	#for key in vertCompressed:
	#	for ln in vertCompressed[key]:
	#		for x1,y1,x2,y2 in ln:
	#			cv2.line(mazeImg2,(x1,y1),(x2,y2),(0,255,0),2)	#Draw horizontal lines Green
	#import random
	#cv2.imshow(str(random.randint(1,1000)), mazeImg2)
	
	#Find start and end points of maze	
	#Point, followed by distance from edge
	minXPt1 = ((float("inf"), 0), 0)
	maxXPt1 = ((-1, 0), 0)
	minYPt1 = ((0, float("inf")), 0)
	maxYPt1 = ((0, -1), 0)
	
	minXPt2 = ((float("inf"), 0), 0)
	maxXPt2 = ((-1, 0), 0)
	minYPt2 = ((0, float("inf")), 0)
	maxYPt2 = ((0, -1), 0)
	
	imgRows,imgCols = mazeImg.shape
	
	for key in horizCompressed:
		for ln in horizCompressed[key]:
			for x1,y1,x2,y2 in ln:
				if x1 > -1 and x1 < imgCols and y1 > -1 and y1 < imgRows and (minXPt1[0] != (x1,y1)) and (minXPt2[0] != (x1,y1)) and (maxXPt1[0] != (x1,y1)) and (maxXPt2[0] != (x1,y1)):
					if x1 < minXPt1[0][0]:
						minXPt2 = minXPt1
						minXPt1 = ((x1,y1), x1)
					elif x1 < minXPt2[0][0]:
						minXPt2 = ((x1,y1), x1)
					if x1 > maxXPt1[0][0]:
						maxXPt2 = maxXPt1
						maxXPt1 = ((x1,y1), imgCols - x1)
					elif x1 > maxXPt2[0][0]:
						maxXPt2 = ((x1,y1), imgCols - x1)
				if x2 > -1 and x2 < imgCols and y2 > -1 and y2 < imgRows and (minXPt1[0] != (x2,y2)) and (minXPt2[0] != (x2,y2)) and (maxXPt1[0] != (x2,y2)) and (maxXPt2[0] != (x2,y2)):		
					if x2 < minXPt1[0][0]:
						minXPt2 = minXPt1
						minXPt1 = ((x2,y2), x2)
					elif x2 < minXPt2[0][0]:
						minXPt2 = ((x2,y2), x2)
					if x2 > maxXPt1[0][0]:
						maxXPt2 = maxXPt1
						maxXPt1 = ((x2,y2), imgCols - x2)
					elif x2 > maxXPt2[0][0]:
						maxXPt2 = ((x2,y2), imgCols - x2)
	for key in vertCompressed:
		for ln in vertCompressed[key]:
			for x1,y1,x2,y2 in ln:	
				if x1 > -1 and x1 < imgCols and y1 > -1 and y1 < imgRows and (minYPt1[0] != (x1,y1)) and (minYPt2[0] != (x1,y1)) and (maxYPt1[0] != (x1,y1)) and (maxYPt2[0] != (x1,y1)): 
					if y1 < minYPt1[0][1]:
						minYPt2 = minYPt1
						minYPt1 = ((x1,y1), y1)
					elif y1 < minYPt2[0][1]:
						minYPt2 = ((x1,y1), y1)
					if y1 > maxYPt1[0][1]:
						maxYPt2 = maxYPt1
						maxYPt1 = ((x1,y1), imgRows - y1)
					elif y1 > maxYPt2[0][1]:
						maxYPt2 = ((x1,y1), imgRows - y1)
				if x2 > -1 and x2 < imgCols and y2 > -1 and y2 < imgRows and (minYPt1[0] != (x2,y2)) and (minYPt2[0] != (x2,y2)) and (maxYPt1[0] != (x2,y2)) and (maxYPt2[0] != (x2,y2)):	
					if y2 < minYPt1[0][1]:
						minYPt2 = minYPt1
						minYPt1 = ((x2,y2), y2)
					elif y2 < minYPt2[0][1]:
						minYPt2 = ((x2,y2), y2)
					if y2 > maxYPt1[0][1]:
						maxYPt2 = maxYPt2
						maxYPt1 = ((x2,y2), imgRows - y2)
					elif y2 > maxYPt2[0][1]:
						maxYPt2 = ((x2,y2), imgRows - y2)
	
	#If no points were found for these mins and maxes, replace with default values
	if float("inf") in minXPt1[0]:
		minXPt1 = ((0,0), 0)
	if -1 in maxXPt1[0]:
		maxXPt1 = ((0,0), 0)
	if float("inf") in minYPt1[0]:	
		minYPt1 = ((0,0), 0)
	if -1 in maxYPt1[0]:
		maxYPt1 = ((0,0), 0)
	
	if float("inf") in minXPt2[0]:
		minXPt2 = ((0,0), 0)
	if -1 in maxXPt2[0]:
		maxXPt2 = ((0,0), 0)
	if float("inf") in minYPt2[0]:	
		minYPt2 = ((0,0), 0)
	if -1 in maxYPt2[0]:
		maxYPt2 = ((0,0), 0)
	
	pts = sorted([minXPt1, maxXPt1, minYPt1, maxYPt1, minXPt2, maxXPt2, minYPt2, maxYPt2], key=lambda x: x[1])
	start = pts[0][0]
	end = pts[1][0]

	return (start,end)		

################################################################
"""
Finds outline of maze and returns triple containing the thresholded image, the 
 original supplied image with the box drawn on it, and the actual points representing the box

params:
	image: The entire raw image taken in by the webcam
	contourThreshVal: Threshold value to use when thresholding the image (taken from slider)
	minBoundBoxVal: Minimum allowed bounding box value (taken from slider)
	
returns:
	(thresh,image,box):
		thresh: Thresholded image (to be used to crop maze from whole image)
		image: Original image with bounding boxes drawn on (to be displayed)
		box: Coordinates of bounding box (to be used to crop maze from whole image)
"""
################################################################
#Finds outline of maze and returns triple containing the thresholded image, the 
# original supplied image with the box drawn on it, and the actual points representing the box
def getMazeOutlineImage(image, contourThreshVal, minBoundBoxVal):		
	#Convert image to grayscale and then threshold it (only black/white pixels)
	BWImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#Probably have a slider or something for the threshold value (right now its set statically to 190)
	ret,thresh = cv2.threshold(BWImage,contourThreshVal,255,cv2.THRESH_BINARY_INV)

	#Contour the image (find all outlines) and use that info to get all possible surrounding boxes around
	# the maze. This eliminates all background 'noise' so just the maze can be focused on
	im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	box = np.array([])
	boxes = []	
	for cnt in contours:
		rect = cv2.minAreaRect(cnt)
		
		#Make sure rect is big enough to bother considering
		if rect[1][0]*rect[1][1] < minBoundBoxVal:
			continue

		box = cv2.boxPoints(rect)
		box = np.int0(box)
		boxes.append(box)
		cv2.drawContours(image,[box],0,(0,255,0),3) #Draw each bounding box for testing
	
	#If more than 1 surrounding box was found, combine the boxes to get actual outline of maze.
	"""
	NOTE:
		For many mazes, even after background noise has been eliminated above, opencv will find 2+
		surrounding rectangles that each surround part of the maze. The below code
		combines boxes to create one surrounding rectangle for the whole maze
	"""	
	if len(boxes) > 0:
		boxpts = []
		for b in boxes:
			for pt in b:
				boxpts.append(pt)
		newRect = cv2.minAreaRect(np.array([boxpts]))		
		box = cv2.boxPoints(newRect)
		box = np.int0(box)	
	
	#If no maze was found, return None
	if box.size == 0:
		return (None,None)
	
	#Draw maze outline onto image	
	cv2.drawContours(image,[box],0,(0,0,255),3) 
	
	thresh = cv2.bitwise_not(thresh) #Also return uninverted threshold image (to be used later)
	return (thresh,image,box)

################################################################
"""
Take an image and a bounding box, and return the parts of the image contained within the bounding box
 with its orientation corrected to be an unrotated rectangle

params:
	thresh: Thresholded version of the entire raw image taken in by the webcam
	box: Coordinates of the bounding box of the maze

returns:
	dst2,h:
		dst2: The cropped maze image (Just the maze taken from the whole raw image)
		h: the homography matrix used to retranslate pixels from cropped image onto the original image
			(used later to overlay the solution onto the original image in the GUI)
"""
################################################################	
def getImageFromBox(thresh, box):
	#Take the now surrounded area (the maze minus the background) and crop that from the whole image
	# to create a new image of JUST the maze
	
	#If bottomLeft = true, boxPoints[0] corresponds to btm-lft corner of subImage. 
	#If bottomLeft = false, boxPoints[0] corresponds to btm-right corner of subImage.
	bottomLeft = True

	newImageRotRect = cv2.minAreaRect(box)

	#Take care of 0.0/-90.0 degree corner-confusion
	if newImageRotRect[2] == 0 or newImageRotRect[2] == -90:
		if abs(box[1][1] - box[0][1]) < 10:
			bottomLeft = False
		newImageRotRect = (newImageRotRect[0], (newImageRotRect[1][1],newImageRotRect[1][0]), -0.000001)
	
	elif newImageRotRect[2] < -45:
		bottomLeft = False
		newImageRotRect = (newImageRotRect[0], (newImageRotRect[1][1],newImageRotRect[1][0]), newImageRotRect[2] + 90)	
	M = cv2.getRotationMatrix2D(newImageRotRect[0], newImageRotRect[2], 1.0)	
	size = np.int0(newImageRotRect[1])
	size = (size[0],size[1])
	dst = cv2.warpAffine(thresh, M, (thresh.shape[1], thresh.shape[0]))
	dst2 = cv2.getRectSubPix(dst, size, newImageRotRect[0])
	
	#Fix size
	size = (size[1],size[0])
	
	#Get homography matrix
	if bottomLeft:
		pts_src = np.array([[0, size[0] - 1], [0, 0], [size[1] - 1, 0],[size[1] - 1, size[0] - 1]])
	else:
		pts_src = np.array([[size[1] - 1, size[0] - 1], [0, size[0] - 1], [0, 0], [size[1] - 1, 0]])
	pts_dst = box
	h, status = cv2.findHomography(pts_src, pts_dst)

	return dst2,h

################################################################
"""
Solve the maze and return the thresholded image of the maze with the solution overlayed onto it 
 to be displayed on its own. Also return the original raw image (supplied as a param) with the solution
 overlayed on top.

params:
	origImage: Raw image taken from web am
	h: the homography matrix used to retranslate pixels from cropped image onto the original image
	mazeImg: Cropped and thresholded image of just the maze
	erosionVal:	Value to use for erosion of path (taken from slider) 

returns:
	mazeImg,origImage:
		mazeImg: Thresholded maze image with solution overlayed on top
		origImage: Original raw image with solution overlayed on top
"""
################################################################		
def getSolvedMaze(origImage, h, mazeImg, erosionVal):
	
	kernel = np.ones((erosionVal,erosionVal), np.uint8)	
	mazeImg = cv2.erode(mazeImg, kernel, iterations=1)
	ret,mazeImg = cv2.threshold(mazeImg,10,255,cv2.THRESH_BINARY) #rethreshold to help find lines better
	
	#Get start end!
	start,end = findStartEnd(mazeImg)
	
	cv2.circle(mazeImg, start, 4, 255, -1)
	cv2.circle(mazeImg, end, 4, 255, -1)

	#Enlarge start/end points
	imgRows,imgCols = mazeImg.shape
	origRows,origCols,_ = origImage.shape
	
	#Solve!
	problem = mazeSearch.MazeSearchProblem(mazeImg, imgRows, imgCols, start, end)
	solution = mazeSearch.aStarSearch(problem, mazeSearch.mazeSearchheuristic)

	#Draw start/end and convert image to color
	mazeImg = cv2.cvtColor(mazeImg, cv2.COLOR_GRAY2BGR)
	cv2.circle(mazeImg, start, 5, (255,0,0), 5)
	cv2.circle(mazeImg, end, 5, (255,0,0), 5)
    
	#Draw solution (on cropped and original image)
	pxs = [] #Pixels to be translated to the original images pixels
	state = start
	mazeImg[state[1]][state[0]] = (0,255,0)
	for action in solution:
		x,y = problem.getNextState(state, action)
		state = (x,y)
		pt1 = ((x-1 if x-1>-1 else 0),(y-1 if y-1>-1 else 0))
		pt2 = ((x+1 if x+1<imgCols else imgCols - 1),(y+1 if y+1<imgRows else imgRows - 1))
		cv2.rectangle(mazeImg, pt1, pt2, (0,255,0), -1)
		pxs.append([x,y])
	
	if not not pxs:
		a = np.array(pxs, dtype='float32')
		a = np.array([a])
		pointsOut = cv2.perspectiveTransform(a, h)
		pointsOut = pointsOut[0]
		
		for pt in pointsOut:
			x = int(pt[0])
			y = int(pt[1])
			pt1 = ((x-1 if x-1>-1 else 0),(y-1 if y-1>-1 else 0))	
			pt2 = ((x+1 if x+1<origCols else origCols - 1),(y+1 if y+1<origRows else origRows - 1))
			cv2.rectangle(origImage, pt1, pt2, (0,255,0), -1)

	return mazeImg,origImage
