"""

view.py
-------

Alex Robbins, Andrew Hart
Intro to AI Section 1
Final Project (Maze Solver)


This file defines the GUI. All image updates also happen here in the loop function of the 
Application class.

"""

import PIL.Image
from PIL import ImageTk
from Tkinter import *
import cv2
import cam
import imaging

	
class Application(Frame):
	def createWidgets(self):	
		leftframe = Frame(self.root)
		leftframe.pack( side = LEFT )
		rightframe = Frame(self.root)
		rightframe.pack( side = RIGHT )
		
		topframe = Frame(rightframe)
		topframe.pack( side = TOP )
		bottomframe = Frame(rightframe)
		bottomframe.pack( side = BOTTOM )
		
		self.ThreshSliderLbl = Label(leftframe, text="Threshold Slider", pady=0)
		self.ThreshSliderLbl.grid(row=0, column=0)
		self.ThreshSlider = Scale(leftframe, from_=0, to=255, orient=HORIZONTAL, length=500, variable=self.contourThreshVal)
		self.ThreshSlider.grid(row=1, column=0)
		
		self.MinBoundBoxSliderLbl = Label(leftframe, text="Minimum Allowed Bounding-Box", pady=0)
		self.MinBoundBoxSliderLbl.grid(row=2, column=0)
		self.MinBoundBoxSlider = Scale(leftframe, from_=0, to=100000, orient=HORIZONTAL, length=500, variable=self.minBoundBoxVal)
		self.MinBoundBoxSlider.grid(row=3, column=0)
		
		self.ErosionSliderLbl = Label(leftframe, text="Erosion Level", pady=0)
		self.ErosionSliderLbl.grid(row=4, column=0)
		self.ErosionSlider = Scale(leftframe, from_=0, to=55, orient=HORIZONTAL, length=500, variable=self.erosionVal)
		self.ErosionSlider.grid(row=5, column=0)
		
		self.MainImgLbl = Label(leftframe, text="Original Image", padx=10)
		self.MainImgLbl.grid(row=6, column=0, sticky=W)
		
		resW = self.vc.video.get(3)
		resH = self.vc.video.get(4)
		
		"""
		Set this to whatever the Width of the Main image should be. The height will
		them be set to match the aspect ratio of the web cam so the image is not
		distorted
		"""
		self.MainImgWidth = 700	#Explained above
		self.MainImgHeight = int(self.MainImgWidth*resH/resW) #Calculate height
		
		self.SearchImgWidth = int(self.MainImgWidth*0.75)
		self.SearchImageHeight = int(self.MainImgHeight*0.75)
		
		self.MainImg = Label(leftframe, height=self.MainImgHeight, width=self.MainImgWidth, bg="lightgray")
		self.MainImg.grid(row=7, column=0, sticky=W)
		
		#self.SolveButton = Button(leftframe, text="Solve", fg="#004d1a", bg="lightgray")
		#self.SolveButton.grid(row=8, column=0)
		
		self.SearchImgLbl = Label(topframe, text="Find Maze", padx=10)
		self.SearchImgLbl.grid(row=0, column=0, sticky=W)
		self.SearchImg = Label(topframe, height=10, width=25, bg="lightgray")
		self.SearchImg.grid(row=1, column=0, sticky=W)
		
		self.SolvedImgLbl = Label(bottomframe, text="Solved Maze", padx=10)
		self.SolvedImgLbl.grid(row=0, column=0, sticky=W)
		self.SolvedImg = Label(bottomframe, height=10, width=25, bg="lightgray")
		self.SolvedImg.grid(row=1, column=0, sticky=W)

	def __init__(self, vc, master=None):
		Frame.__init__(self, master)
		self.vc = vc
		self.contourThreshVal = IntVar()
		self.minBoundBoxVal = IntVar()
		self.erosionVal = IntVar()
		self.pack()
		self.root = master
		self.createWidgets()
		self.contourThreshVal.set(60)
		self.minBoundBoxVal.set(5000)
		self.erosionVal.set(20)

	#This is the main loop that updates the images on the GUI	
	def loop(self):		

		#Get/Set main image from web cam
		pilImage, img = self.vc.get_frame()
		img2 = pilImage.resize((self.MainImgWidth, self.MainImgHeight), PIL.Image.ANTIALIAS)
		img2 = ImageTk.PhotoImage(img2)
		self.MainImg.config(image=img2)
		self.MainImg.image = img2
		
		#Get/Set outlined image of maze
		ret = imaging.getMazeOutlineImage(img.copy(), self.contourThreshVal.get(), self.minBoundBoxVal.get())
		if (len(ret) == 3):
			thresh,outline,box = ret
			w = self.SearchImgWidth
			h = self.SearchImageHeight
			self.SearchImg.config(width=w, height=h)				
			pilOutlineImage = PIL.Image.fromarray(cv2.cvtColor(outline,cv2.COLOR_BGR2RGB))
			img2 = pilOutlineImage.resize((w, h), PIL.Image.ANTIALIAS)
			img2 = ImageTk.PhotoImage(img2)
			self.SearchImg.config(image=img2)
			self.SearchImg.image = img2
			
			#Get/Set solved maze! 	
			
			#Get the cropped maze image
			croppedImg,h_Arr = imaging.getImageFromBox(thresh, box)
			
			#Solve it! and get solved image
			solvedImg,origImgSolOverlay = imaging.getSolvedMaze(img, h_Arr, croppedImg, self.erosionVal.get())
			
			#origImgSolOverlay is the original image with the solution overlayed on top. redisplay that in the main image location
			pilOrigImgSolOverlay = PIL.Image.fromarray(cv2.cvtColor(origImgSolOverlay,cv2.COLOR_BGR2RGB))
			pilOrigImgSolOverlay = pilOrigImgSolOverlay.resize((self.MainImgWidth, self.MainImgHeight), PIL.Image.ANTIALIAS)
			pilOrigImgSolOverlay = ImageTk.PhotoImage(pilOrigImgSolOverlay)
			self.MainImg.config(image=pilOrigImgSolOverlay)
			self.MainImg.image = pilOrigImgSolOverlay
			
			#Display cropped image
			self.SolvedImg.config(width=w, height=h)
			pilSolvedImage = PIL.Image.fromarray(solvedImg)
			#Calculate new dimensions of maze to display it with its correct aspect ratio
			solvedImgW,solvedImgH = pilSolvedImage.size
			scale = min( float(w)/solvedImgW, float(h)/solvedImgH)
			newW = int(solvedImgW * scale)
			newH = int(solvedImgH * scale)
			img2 = pilSolvedImage.resize((newW, newH), PIL.Image.ANTIALIAS)
			img2 = ImageTk.PhotoImage(img2)
			self.SolvedImg.config(image=img2)
			self.SolvedImg.image = img2
			
		else: #If no boxes found
			self.SearchImg.config(image=None)			#Set image to none (freezes it)
			self.SolvedImg.config(image=None)			#Set image to none (freezes it)
		
		self.root.after(10, self.loop)  # reschedule event every 0.01 seconds	
	
