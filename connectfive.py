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
		if x > self.size-1 and y > self.size-1:
			return False
		# otherwise if no stone already placed at desired spot
		if self.board[x][y] == 0:
			self.board[x][y] = self.currentTurn
			self.checkWin(x, y) # checks if the game has been won
			self.currentTurn = -self.currentTurn # switch current turns
			return True
		else:
			return False

	# checks if the board has been won by considering only the last move played
	def checkWin(self, x, y):
		# check row

		# check column

		# check upper left-lower right diagonal

		# check upper right-lower left diagonal
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

class App(object):
    def __init__(self, root):
    	## game parameters
    	self.size = 15
    	self.gridSize = 40 #pixels
    	self.width = (self.size+1)*self.gridSize
    	self.height = (self.size+1)*self.gridSize

    	## game initialization
    	self.board = ConnectFiveBoard(self.size)
    	
    	## graphics components initialization
    	self.frame = Frame(root)
    	self.player = StringVar()
    	self.player.set("To move: black")
    	self.playerLabel = Label(root, textvariable=self.player)
    	self.playerLabel.pack()

    	self.w = Canvas(root, width=self.width, height=self.height)
    	self.w.pack()
    	for i in xrange(15):
    		self.w.create_line(0, (i+1)*self.gridSize, self.width, (i+1)*self.gridSize)
    		self.w.create_line((i+1)*self.gridSize, 0, (i+1)*self.gridSize, self.height)

    def mouseClicked(self, event):
    	#print "clicked at", event.x, event.y
    	x = int(round(event.y / float(self.gridSize)) - 1)
    	y = int(round(event.x / float(self.gridSize)) - 1)
    	#print "move: ", str(x), str(y)

    	legal = self.board.playMove(x, y)
    	if legal:
    		print self.board
    		self.player.set("To move: " + self.board.getCurrentPlayerColor())
	    	r = 20
	    	drawX = (x+1)*40
	    	drawY = (y+1)*40
	    	self.w.create_oval(drawY-r, drawX-r, drawY+r, drawX+r, fill=('white' if self.board.getCurrentPlayerColor() == 'black' else 'black'))

if __name__ == '__main__':
	root = Tk()
	application = App(root)
	print("Welcome to Connect 5!")
	root.bind_all('<Button-1>', application.mouseClicked)
	root.mainloop()
	

	# http://stackoverflow.com/questions/14595284/python-tkinter-arrow-key-input-code-not-functioning
