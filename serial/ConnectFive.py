import ConnectFiveMiniMax




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
    	for i in xrange(self.size):
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
    			#self.root.destroy()







if __name__ == '__main__':
	print("Welcome to Connect 5!")
	boardGraphics = ConnectFiveGraphics()