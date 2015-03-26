from compiler.ast import flatten
import sys, random, time

class Sudoku(object):

	blank = 0

	def __init__(self, puzzle=None):
		self.grid = self.makeGrid(puzzle)

	def makeGame(self):
		"""creates a randomly generated game"""
		random.seed(time.time())
		self.grid = self.makeGrid()

		for x in range(8):
			for y in range(8):
				while True: # loop until the selection is valid
					if random.randint(1, 2) == 2:
						self.grid[x][y] = random.randint(1, 9)
					if self.valid() == True:
						break

	def makeGrid(self, puzzle=None): 
		"""creates a sudoku grid from a txt of numbers"""
		if puzzle == None:
			return [[0 for i in range(8)] for i in range(8)]
		grid = []
		p = open(puzzle)
		for line in p.read().splitlines():
			grid.append([int(i) for i in line.split()])
		return grid

	def valid(self): 
		"""Runs conflict checkers. Returns False if conflict"""
		return self.checkRow() and self.checkCol() and self.checkSquare()

	def checkRow(self): 
		"""checks all rows for conflicts"""
		for y in range(8):
			cpy = [i for i in self.grid[y] if i != self.blank] #create a copy of the row with all empty spaces removed
			if len(cpy) != len(set(cpy)): return False #check if the row has duplicate values. Returns True if valid
		return True

	def checkCol(self): 
		"""checks all cols for conflicts"""
		for x in range(8):
			cpy = [i[x] for i in self.grid if i[x] != self.blank] # create a copy of col with all empty spaces removed
			if len(cpy) != len(set(cpy)): return False #check if the col has duplicate values. Returns True if valid
		return True

	def checkSquare(self): 
		"""checks all 3x3 blocks for conflicts"""
		for y in range(3):
			for x in range(3):
				cpy = [i for i in flatten([bb[y*3:y*3+3] for bb in self.grid[x*3:x*3+3]]) if i != self.blank]
				if len(cpy) != len(set(cpy)):
					return False
		return True

	def solve(self, x=0, y=0, silent=True):
		if (x, y) == (9, 8): #check for compleated grid
			return True
		elif x == 9: #if the row has been compleated, continue to the next one
			x, y = 0, y+1
		if silent == False: #option for non-silent mode
			print x, y
			print self.grid
															 
		if s.grid[x][y] == 0: #if slot is empty
			for i in range(1, 10): #for possible entry
				self.grid[x][y] = i #set slot to possible entry
				if self.valid(): #check if the grid is valid
					if self.solve(x=x+1, y=y, silent=silent): #recursivly check the next slot
						return True
			self.grid[x][y] = 0
		else: #if the currnet slot was already occupied, go to next slot
			if self.solve(x=x+1, y=y, silent=silent):
				return True
		return False #return False if there's no current solutions for this slot/if the puzzle is unsolvable

if __name__ == '__main__':
	try:
		s = Sudoku(sys.argv[1])
		print s.solve(silent=False)
		print s.grid
	except:
		print 'please provide a sudoku problem'
