"""

main.py	
-------

Alex Robbins, Andrew Hart
Intro to AI Section 1
Final Project (Maze Solver)


This is the main file to be called on startup. It creates a new GUI window
and does everything else that needs to be done.

HOW-TO:
	1.) Start this program
	2.) Point camera at a maze image on a flat surface
	3.) Adjust the 3 sliders until solution is constantly overlayed on top of the maze image
		3a.) Threshold slider controls what level of lightness in a pixel corresponds to a path
		3b.) Minimum Allowed Bounding-Box slider controls the minimum bounding box to be considered as valid when the 
				program is searching for the maze. If for example, there is a small amount of noise in the field of view
				of the camera that is being surrounded by a green box and thus being included in the final bounding
				box of the maze (in turn messing up the finding of the maze), raise the value of this slider until that
				small box is ignored.
		3c.) Erosion Level slider controls how much of the path is eroded away before trying to solve the maze. For mazes 
				with thick white paths, set this to a high value. For mazes with a skinny white path, set this to a low value.

RULES:
	1.) Maze should be completely within the field of view of the camera
	2.) Maze must be rectangular in shape
	3.) Maze must have EXACTLY 2 entry points (an entrance/start and an exit/end)
		3a.) Entry points do not need to be labeled in any way. They just need to exist
	4.) Travelable path must be a light color and walls must be a dark color	
	
"""

from Tkinter import *
import mazeSearch
import util
import argparse
import imaging
import view
import cam

vc = cam.VideoCamera()
root = Tk()
root.title("Maze Solver")
app = view.Application(vc, master=root)
root.after(0, app.loop)
app.mainloop()
vc.__del__()
