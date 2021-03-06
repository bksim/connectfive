from ConnectFiveMiniMax import ConnectFiveGameState
from ConnectFiveMiniMax import AlphaBetaAgent
from Tkinter import *
import copy
import time

class ConnectFiveGraphics():
    def __init__(self, gameState, activateAI=False):
    	## game parameters
    	self.gameState = gameState
    	self.activateAI = activateAI
    	self.size = gameState.size

    	self.gridSize = 40 #pixels
    	self.width = (self.size+1)*self.gridSize
    	self.height = (self.size+1)*self.gridSize

        # add turn timer/default time
        self.time = time.time()
    	
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

        self.time = time.time()
    	x = int(round(event.y / float(self.gridSize)) - 1)
    	y = int(round(event.x / float(self.gridSize)) - 1)
    	print "move: ", str(x), str(y)

    	currentTurn = self.gameState.currentTurn
    	# if legal
    	if (x, y) in self.gameState.getLegalActions(currentTurn):
            self.playMove((x, y))

            # make an AI agent
            alphabeta_agent = AlphaBetaAgent(depth=2)
            # get ai's move
            ai_move = alphabeta_agent.getAction(copy.deepcopy(self.gameState), -1)
            print "AI WOULD NOW PLAY: " + str(ai_move)
            print "Time: " + str(time.time() - self.time)
            # play ai's move for it if necessary
            if self.activateAI:
                self.playMove(ai_move)

    def drawMove(self, action, currentTurn):
    	r = 20
    	drawX = (action[0]+1)*40
    	drawY = (action[1]+1)*40
    	self.w.create_oval(drawY-r, drawX-r, drawY+r, drawX+r, fill=('white' if currentTurn == -1 else 'black'))

    def playMove(self, action):
    	currentTurn = self.gameState.currentTurn
    	self.gameState = self.gameState.generateSuccessor(currentTurn, action)
    	if self.gameState.isOver():
    	    winnerString = "black" if self.gameState.getWinner() == 1 else "white"
    	    print "GAME OVER - WINNER IS: " + winnerString
            self.player.set("GAME OVER - WINNER IS: " + winnerString)
        toMoveString = "black" if currentTurn == -1 else "white"
        self.player.set("To move: " + toMoveString)
        self.drawMove(action, currentTurn)

if __name__ == '__main__':
    print("Welcome to Connect 5!")
    size = 15
    clean_board = [x[:] for x in [[0]*size]*size]
    spiral = []
    start = (int(size / 2), int(size / 2))
    spiral.append(start)
    side_length = 1
    
    while spiral[-1] != (0,0):
    	f = 1 if side_length % 2 == 1 else -1
	for i in range(side_length):
	    spiral.append((spiral[-1][0]+f, spiral[-1][1]))
	for j in range(side_length):
	    spiral.append((spiral[-1][0], spiral[-1][1]+f))
        side_length+=1
    for i in range(1, int(size)):
    	spiral.append((i, 0))
	
    gameState = ConnectFiveGameState(clean_board, 1, moveOrdering=spiral)
    boardGraphics = ConnectFiveGraphics(gameState, activateAI=True)
