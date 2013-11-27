import copy

class ConnectFiveGameState:
	def __init__(self, board, currentTurn):
		self.currentTurn = currentTurn
		self.board = board
		self.size = len(board)

	def isOver():
		# wesley will fill this in
		return True

	# returns a list of tuples, where each tuple is a legal move
	def getLegalActions(agentIndex):
		legal_actions = []
		for row in xrange(self.size):
			for col in xrange(self.size):
				if self.board[row][col] == 0:
					legal_actions.append((row, col))
		return legal_actions

	def generateSuccessor(self, agentIndex, action):
		new_board = copy.deepcopy(self.board)
		new_board[action[0]][action[1]] = agentIndex
		successor = ConnectFiveGameState(new_board, -agentIndex)
		return successor


# minimax agent
class MinimaxAgent:
	def __init__(self, depth=2):
		# fill in stuff here
		self.depth = depth

	# terminal test
	def is_terminal(self, gameState):
		return gameState.isOver()

	def evaluationFunction(self, gameState):
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
			v = min(v, self.maxValue(gameState,generateSuccessor(agentIndex, action), \
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
	clean_board = [x[:] for x in [[0]*size]*size]
	gameState = ConnectFiveGameState(clean_board, 1)
	minimax_agent.getAction(gameState, -1)