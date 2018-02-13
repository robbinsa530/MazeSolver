"""

mazeSearch.py
-------------

Alex Robbins, Andrew Hart
Intro to AI Section 1
Final Project (Maze Solver)

This file contains all the classes and functions used to solve the maze. Mazes are solved by 
 searching through white pixels, using non-white pixels as inpenetrable walls. Search is done with
 the A* algorithm using distance from pixel to exit as a heuristic.
 
NOTE: Although this code is heavily modified to be specific to our problem, the basic structure of it 
		was taken from the UC Berkeley Pacman AI Project, and credit for that goes to John DeNero and Dan Klein

"""

import util
import time

class Directions:
    LEFT = 'Left'
    RIGHT = 'Right'
    UP = 'Up'
    DOWN = 'Down'

################################################################
"""
Used to solve a general graph search problem. Used here with A* algorithm to solve mazes.
This implementation of graph search sets a time limit of 3 seconds on the solve. If no 
 solution is found in those 3 seconds, an empty list is returned.

params:
	problem: Search problem
	frontier: Data structure to use for searching for solution to problem
	
returns:
	empty list if no solution, or a solution to the search problem in the form of a list of actions
"""
################################################################	
def graphSearch(problem, frontier):
	#'closed' set starts off empty (use set to improve speed)
	closed = set([])
	#Initiate the frontier/fringe list with the start node for the problem.
	#Each node will be a tuple containing: state, actions to get to state, cost of action list
	#Because this is the start state, the associated actions list will be empty and cost will be the related cost of 0 actions given the problem
	frontier.push((problem.getStartState(), [], problem.getCostOfActions([])))
	
	#Place time limit on solve
	t = time.time()
	tEnd = t + 3
	
	#import cv2 ##TEST
	#mz = problem.maze.copy() ##TEST
	#mz = cv2.cvtColor(mz, cv2.COLOR_GRAY2BGR) ##TEST

	while True:
		if time.time() > tEnd:
			#print "Time limit reached" ##TEST
			#cv2.imshow("testtt", mz) ##TEST
			return []
		if frontier.isEmpty():
			#print "No solution found" ##TEST
			#cv2.imshow("testtt", mz) ##TEST
			return [] #Failure (path not found)
		node = frontier.pop()
		if problem.isGoalState(node[0]):
			#print "Solution found" ##TEST
			
			#imgRows,imgCols,_ = mz.shape
			#state = problem.startState
			#for action in node[1]:
			#	x,y = problem.getNextState(state, action)
			#	state = (x,y)
			#	pt1 = ((x-1 if x-1>-1 else 0),(y-1 if y-1>-1 else 0))
			#	pt2 = ((x+1 if x+1<imgCols else imgCols - 1),(y+1 if y+1<imgRows else imgRows - 1))
			#	cv2.rectangle(mz, pt1, pt2, (0,255,0), -1)
			#cv2.imshow("testtt", mz) ##TEST
			
			return node[1] #Path found! return the actions list of the node which contained the goal state
		#If the state checked was not the goal state, add it to the 'closed' list, and get all the successor states of the state checked
		if not (node[0] in closed):
			closed.add(node[0])
			#mz[node[0][1]][node[0][0]] = (255,122,0) ##TEST
			for triple in problem.getSuccessors(node[0]):
				frontier.push((triple[0], node[1] + [triple[1]], node[2] + triple[2]))
	
def aStarSearch(problem, heuristic=(lambda x,y: 0)):
	"""Search the node that has the lowest combined cost and heuristic first."""
	#Priority Queue function takes a node and returns the total cost to get from start state to node state.
	# This value is then added to the value returned by the heuristic function
	return graphSearch(problem, util.PriorityQueueWithFunction(lambda node: node[2] + heuristic(node[0], problem)))
	
################################################################
"""
Our actual maze search problem. Problems consist of:
	maze: Thresholded image of the maze to be solved
	rows: # of rows in the maze
	cols: # of cols in the maze
	start: Start point of maze as an x,y coordinate
	end: End point of maze as an x,y coordinate
"""
################################################################		
class MazeSearchProblem:
	
	def __init__(self, maze, rows, cols, start, end):
		#Maze is an image representing the board with 255 = corridors and all else being walls
		self.rows = rows
		self.cols = cols
		self.maze = maze	
		self.startState = start
		self.endState = end
		
	def getStartState(self):	
		return self.startState
	
	#Checks if current state = end location
	def isGoalState(self, state):
		return state == self.endState
	
	#Returns all valid successors (successors not out of the bounds of the maze image)
	def getSuccessors(self, state):
		left  = (state[0] - 1, state[1])
		right = (state[0] + 1, state[1]) 
		above = (state[0], state[1] - 1)
		below = (state[0], state[1] + 1)
		
		successors = []

		if (-1 not in left) and self.maze[left[1]][left[0]] == 255:
			successors.append((left, Directions.LEFT, 1))
		if (self.cols != right[0]) and self.maze[right[1]][right[0]] == 255:
			successors.append((right, Directions.RIGHT, 1))
		if (-1 not in above) and self.maze[above[1]][above[0]] == 255:
			successors.append((above, Directions.UP, 1))
		if (self.rows != below[1]) and self.maze[below[1]][below[0]] == 255:
			successors.append((below, Directions.DOWN, 1))
		
		return successors
		
	#All actions have cost of 1	
	def getCostOfActions(self, actions):
		return len(actions)
		
	def getNextState(self, state, action):
		if action == Directions.LEFT:
			return (state[0] - 1, state[1])
		if action == Directions.RIGHT:
			return (state[0] + 1, state[1])
		if action == Directions.UP:
			return (state[0], state[1] - 1)
		if action == Directions.DOWN:
			return 	(state[0], state[1] + 1)

#Heuristic is just distance from location to end			
def mazeSearchheuristic(state, problem):
	x,y = state
	x2,y2 = problem.endState
	return abs(x - x2) + abs(y - y2)
