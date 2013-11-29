import copy

class ConnectFiveGameState:
	def __init__(self, board, currentTurn, firstPlayerHeuristic=None, secondPlayerHeuristic=None, lastMovePlayed=None):
		self.currentTurn = currentTurn
		self.board = board
		self.size = len(board)
		self.firstPlayerHeuristic = {}
		self.secondPlayerHeuristic = {}
		self.lastMovePlayed = None

	def isOver(self):
		# Check if either player has a 5 in a row or greater
		if (self.firstPlayerHeuristic and self.secondPlayerHeuristic and 
			(self.firstPlayerHeuristic[4] > 0 or self.secondPlayerHeuristic[4] > 0)):
			return True
		return False


    '''TODO: Check logic of this/try it'''
	# counter of X-in-a-row heursitic
	def updateXinARowHeuristic(self):
		# for each type of search, ex: vertical, count how many are the same piece and directly above and below - subtract from those values in the heuristic and add to the value of upper+lower+1

		# search vertical
		upperChain = 0
		lowerChain = 0
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] - offset, self.lastMovePlayed[1]] == self.currentTurn:
				upperChain += 1
			else:
				break
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] + offset, self.lastMovePlayed[1]] == self.currentTurn:
				lowerChain += 1
			else:
				break
	    if self.currentTurn == 1:
	    	self.firstPlayerHeuristic[upperChain] -= 1
	    	self.firstPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.firstPlayerHeuristic[4] += 1
	    	else:
	    		self.firstPlayerHeuristic[upperChain + lowerChain + 1]
		else:
	    	self.secondPlayerHeuristic[upperChain] -= 1
	    	self.secondPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.secondPlayerHeuristic[4] += 1
	    	else:
	    		self.secondPlayerHeuristic[upperChain + lowerChain + 1]

		# search horizontal
		upperChain = 0
		lowerChain = 0
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0], self.lastMovePlayed[1] - offset] == self.currentTurn:
				upperChain += 1
			else:
				break
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0], self.lastMovePlayed[1] + offset] == self.currentTurn:
				lowerChain += 1
			else:
				break
	    if self.currentTurn == 1:
	    	self.firstPlayerHeuristic[upperChain] -= 1
	    	self.firstPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.firstPlayerHeuristic[4] += 1
	    	else:
	    		self.firstPlayerHeuristic[upperChain + lowerChain + 1]
		else:
	    	self.secondPlayerHeuristic[upperChain] -= 1
	    	self.secondPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.secondPlayerHeuristic[4] += 1
	    	else:
	    		self.secondPlayerHeuristic[upperChain + lowerChain + 1]

		# search upper left, bottom right diagonal
		upperChain = 0
		lowerChain = 0
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] - offset, self.lastMovePlayed[1] - offset] == self.currentTurn:
				upperChain += 1
			else:
				break
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] + offset, self.lastMovePlayed[1] + offset] == self.currentTurn:
				lowerChain += 1
			else:
				break
	    if self.currentTurn == 1:
	    	self.firstPlayerHeuristic[upperChain] -= 1
	    	self.firstPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.firstPlayerHeuristic[4] += 1
	    	else:
	    		self.firstPlayerHeuristic[upperChain + lowerChain + 1]
		else:
	    	self.secondPlayerHeuristic[upperChain] -= 1
	    	self.secondPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.secondPlayerHeuristic[4] += 1
	    	else:
	    		self.secondPlayerHeuristic[upperChain + lowerChain + 1]

		# search upper right, bottom left diagonal
		upperChain = 0
		lowerChain = 0
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] - offset, self.lastMovePlayed[1] + offset] == self.currentTurn:
				upperChain += 1
			else:
				break
		for offset in xrange (1,5):
			if self.board[self.lastMovePlayed[0] + offset, self.lastMovePlayed[1] - offset] == self.currentTurn:
				lowerChain += 1
			else:
				break
	    if self.currentTurn == 1:
	    	self.firstPlayerHeuristic[upperChain] -= 1
	    	self.firstPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.firstPlayerHeuristic[4] += 1
	    	else:
	    		self.firstPlayerHeuristic[upperChain + lowerChain + 1]
		else:
	    	self.secondPlayerHeuristic[upperChain] -= 1
	    	self.secondPlayerHeuristic[lowerChain] -= 1
	    	if upperChain + lowerChain > 4:
	    		self.secondPlayerHeuristic[4] += 1
	    	else:
	    		self.secondPlayerHeuristic[upperChain + lowerChain + 1]
		
	    return

	# convert heursitic data to a weighted score
    def calcXinARowScore(self):
    	#ADJUSTABLE SCORE WEIGHTINGS
    	scoreWeights = [1,5,25,100,999999999]
    	if self.currentTurn == 1:
    		return self.firstPlayerHeuristic[0] * scoreWeights[0] + self.firstPlayerHeuristic[1] * scoreWeights[1] + self.firstPlayerHeuristic[2] * scoreWeights[2] +  self.firstPlayerHeuristic[3] * scoreWeights[3] + self.firstPlayerHeuristic[4] * scoreWeights[4]
    	else:
    		return self.secondPlayerHeuristic[0] * scoreWeights[0] + self.secondPlayerHeuristic[1] * scoreWeights[1] + self.secondPlayerHeuristic[2] * scoreWeights[2] +  self.secondPlayerHeuristic[3] * scoreWeights[3] + self.secondPlayerHeuristic[4] * scoreWeights[4]


	# returns a list of tuples, where each tuple is a legal move
	def getLegalActions(self, agentIndex):
		legal_actions = []
		for row in xrange(self.size):
			for col in xrange(self.size):
				if self.board[row][col] == 0:
					legal_actions.append((row, col))
		return legal_actions

	# returns a new ConnectFiveGameState given an action taken by some agentIndex
	def generateSuccessor(self, agentIndex, action):
		new_board = copy.deepcopy(self.board)
		new_board[action[0]][action[1]] = agentIndex
		successor = ConnectFiveGameState(new_board, -agentIndex, 
			copy.deepcopy(self.firstPlayerHeuristic), copy.deepcopy(self.secondPlayerHeuristic),
			self.lastMovePlayed)
		return successor

	# returns a dict with keys being the number in a row and values being how many of those
	# opportunities there are
	def getNumInARow(self):
		return self.firstPlayerHeuristic if self.currentTurn == 1 else self.secondPlayerHeuristic

# minimax agent
class MinimaxAgent:
	def __init__(self, depth=2):
		# fill in stuff here
		self.depth = depth

	# terminal test
	def is_terminal(self, gameState):
		return gameState.isOver()

	def evaluationFunction(self, gameState):
		h = gameState.getNumInARow()
		# come up with a heuristic here to evaluate how good a board is
		return 0

	def maxValue(self, gameState, agentIndex, depth):
		if depth == 0 or self.is_terminal(gameState):
			return self.evaluationFunction(gameState)

		v = float("-inf")
		actions = gameState.getLegalActions(agentIndex)
		# calculate for each action all possible new game states
		for action in actions:
			v = max(v, self.minValue(gameState.generateSuccessor(agentIndex, action), \
				-agentIndex, depth))
		return v

	def minValue(self, gameState, agentIndex, depth):
		if depth == 0 or self.is_terminal(gameState):
			return self.evaluationFunction(gameState)

		v = float("inf")
		actions = gameState.getLegalActions(gameState)
		for action in actions:
			v = min(v, self.maxValue(gameState.generateSuccessor(agentIndex, action), \
				-agentIndex, depth-1))
		return v

	def getAction(self, gameState, agentIndex):
		current_best_action = None
		current_best_score = float("-inf")
		actions = gameState.getLegalActions(agentIndex)
		for action in actions:
			newScore = self.minValue(gameState.generateSuccessor(agentIndex, action), -agentIndex, self.depth)
			if newScore > current_best_score:
				current_best_action = action
				current_best_score = newScore
		return current_best_action



if __name__ == '__main__':
	minimax_agent = MinimaxAgent(2)
	size = 15
	clean_board = [x[:] for x in [[0]*size]*size]
	gameState = ConnectFiveGameState(clean_board, 1)
	minimax_agent.getAction(gameState, -1)