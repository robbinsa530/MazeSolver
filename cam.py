"""

cam.py
------

Alex Robbins, Andrew Hart
Intro to AI Section 1
Final Project (Maze Solver)


This file defines the VideoCamera object used to capture images from the webcam
 and use them in our other code.

"""

import cv2
import PIL.Image

class VideoCamera(object):
	def __init__(self):
		#If no external cam: 0 will be webcam
		#If external cam connected: 0 will be external cam and 1 will be webcam
		self.video = cv2.VideoCapture(0)
		#Will set resolution to highest it cam be (assuming it cant be higher than 10,000x10,000)
		self.video.set(3,10000) #Set width
		self.video.set(4,10000) #Set height
		
	def __del__(self):
		self.video.release()
	
	def get_frame(self):
		success, image = self.video.read()
		imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		pilImage = PIL.Image.fromarray(imageRGB)
		
		#pilImage to be displayed, and image to be manipulated
		return pilImage, image