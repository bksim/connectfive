from Tkinter import *

# initial version of connect five game
class ConnectFiveBoard:
	""" a basic connect five board class."""
	def __init__(self, size=15):
		# first player is 1, second player is -1
		self.currentTurn = 1
		self.size = size
		self.board = [x[:] for x in [[0]*size]*size]

	# returns true if move legal
	# returns false if move not legal
	# insert other legality checks here
	def playMove(self, x, y):
		# if stone is off the board then return False
		if x > self.size-1 or y > self.size-1 or x < 0 or y < 0:
			return False
		# otherwise if no stone already placed at desired spot
		if self.board[x][y] == 0:
			self.board[x][y] = self.currentTurn
			if self.checkWin(x, y): # checks if the game has been won
				#print "WINNER: " + self.getCurrentPlayerColor()
				self.currentTurn = -self.currentTurn
				return 'black' if self.getCurrentPlayerColor() == 'white' else 'white'
			self.currentTurn = -self.currentTurn # switch current turns
			return True
		else:
			return False

	# checks if the board has been won by considering only the last move played
	def checkWin(self, x, y):
		# check row: keep x constant, change y
		for checkY in range(5):
			if y-checkY >= 0 and y-checkY+4 <= self.size-1:
				if (self.board[x][y-checkY] == self.currentTurn and
					self.board[x][y-checkY+1] == self.currentTurn and
					self.board[x][y-checkY+2] == self.currentTurn and
					self.board[x][y-checkY+3] == self.currentTurn and
					self.board[x][y-checkY+4] == self.currentTurn):
					return True

		# check column: keep y constant, change x
		for checkX in range(5):
			if x-checkX >= 0 and x-checkX+4 <= self.size-1:
				if (self.board[x-checkX][y] == self.currentTurn and
					self.board[x-checkX+1][y] == self.currentTurn and
					self.board[x-checkX+2][y] == self.currentTurn and
					self.board[x-checkX+3][y] == self.currentTurn and
					self.board[x-checkX+4][y] == self.currentTurn):
					return True				

		# check upper left-lower right diagonal: add 1 to x, add 1 to y
		for check in range(5):
			if x-check >= 0 and x-check+4 <= self.size-1 and y-check >= 0 and y-check+4 <= self.size-1:
				if (self.board[x-check][y-check] == self.currentTurn and
					self.board[x-check+1][y-check+1] == self.currentTurn and
					self.board[x-check+2][y-check+2] == self.currentTurn and
					self.board[x-check+3][y-check+3] == self.currentTurn and
					self.board[x-check+4][y-check+4] == self.currentTurn):
					return True

		# check upper right-lower left diagonal: +1 to x, -1 from y
		for check in range(5):
			if x-check >= 0 and x-check+4 <= self.size-1 and y+check <= self.size-1 and y+check-4 >= 0:
				if (self.board[x-check][y+check] == self.currentTurn and
					self.board[x-check+1][y+check-1] == self.currentTurn and
					self.board[x-check+2][y+check-2] == self.currentTurn and
					self.board[x-check+3][y+check-3] == self.currentTurn and
					self.board[x-check+4][y+check-4] == self.currentTurn):
					return True
		return False

	def __str__(self):
		printString = ""
		for row in self.board:
			printString += (str(row) + '\n')
		return printString

	def getCurrentTurn(self):
		return self.currentTurn

	def getCurrentPlayerColor(self):
		return 'black' if self.currentTurn > 0 else 'white'

#########
class ConnectFiveGraphics():
    def __init__(self):
    	## game parameters
    	self.size = 15
    	self.gridSize = 40 #pixels
    	self.width = (self.size+1)*self.gridSize
    	self.height = (self.size+1)*self.gridSize

    	## game initialization
    	self.board = ConnectFiveBoard(self.size)
    	
    	## graphics components initialization
    	self.root = Tk()
    	self.frame = Frame(self.root)
    	self.player = StringVar()
    	self.player.set("To move: black")
    	self.playerLabel = Label(self.root, textvariable=self.player)
    	self.playerLabel.pack()

    	self.w = Canvas(self.root, width=self.width, height=self.height)
    	self.w.pack()
    	for i in xrange(15):
    		self.w.create_line(0, (i+1)*self.gridSize, self.width, (i+1)*self.gridSize)
    		self.w.create_line((i+1)*self.gridSize, 0, (i+1)*self.gridSize, self.height)

    	self.root.bind_all('<Button-1>', self.mouseClicked)
    	self.root.mainloop()

    def mouseClicked(self, event):
    	#print "clicked at", event.x, event.y
    	x = int(round(event.y / float(self.gridSize)) - 1)
    	y = int(round(event.x / float(self.gridSize)) - 1)
    	#print "move: ", str(x), str(y)

    	legal = self.board.playMove(x, y)
    	if legal:
    		#print self.board
    		self.player.set("To move: " + self.board.getCurrentPlayerColor())
	    	r = 20
	    	drawX = (x+1)*40
	    	drawY = (y+1)*40
	    	self.w.create_oval(drawY-r, drawX-r, drawY+r, drawX+r, fill=('white' if self.board.getCurrentPlayerColor() == 'black' else 'black'))
	    	if legal == 'black' or legal == 'white':
	    		print "GAME OVER: WINNER IS " + legal
    			self.player.set("GAME OVER: WINNER IS " + legal)
    			self.root.destroy()

if __name__ == '__main__':
	print("Welcome to Connect 5!")
	boardGraphics = ConnectFiveGraphics()

	# http://stackoverflow.com/questions/14595284/python-tkinter-arrow-key-input-code-not-functioning
