import copy

class ConnectFiveGameState:
    def __init__(self, board, currentTurn, firstPlayerHeuristic={}, secondPlayerHeuristic={}, lastMovePlayed=None):
        self.currentTurn = currentTurn
        self.board = board
        self.size = len(board)
        self.firstPlayerHeuristic = firstPlayerHeuristic
        self.secondPlayerHeuristic = secondPlayerHeuristic
        self.lastMovePlayed = lastMovePlayed

        if self.firstPlayerHeuristic == {}:
        	self.firstPlayerHeuristic[0] = 0
        	self.firstPlayerHeuristic[1] = 0
        	self.firstPlayerHeuristic[2] = 0
        	self.firstPlayerHeuristic[3] = 0
        	self.firstPlayerHeuristic[4] = 0
        if self.secondPlayerHeuristic == {}:
        	self.secondPlayerHeuristic[0] = 0
        	self.secondPlayerHeuristic[1] = 0
        	self.secondPlayerHeuristic[2] = 0
        	self.secondPlayerHeuristic[3] = 0
        	self.secondPlayerHeuristic[4] = 0

    def isOver(self):
        # Check if either player has a 5 in a row or greater
        if (self.firstPlayerHeuristic and self.secondPlayerHeuristic and 
            (self.firstPlayerHeuristic[4] > 0 or self.secondPlayerHeuristic[4] > 0)):
            return True
        return False

    # counter of X-in-a-row heursitic
    '''Does not do 1 below properly, also starts at -1 for 1 piece....'''
    def updateXinARowHeuristic(self):
        # for each type of search, ex: vertical, count how many are the same piece and directly above and below - subtract from those values in the heuristic and add to the value of upper+lower+1

        isolatedCheck = 0

        # search vertical
        upperChain = 0
        lowerChain = 0
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] - offset < 0:
                break
        	if self.board[self.lastMovePlayed[0] - offset][self.lastMovePlayed[1]] == self.currentTurn:
        		upperChain += 1
        	else:
        		break
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] + offset >= self.size:
                break
            if self.board[self.lastMovePlayed[0] + offset][self.lastMovePlayed[1]] == self.currentTurn:
                lowerChain += 1
            else:
                break
                
        if self.currentTurn == 1:
            if upperChain > 0:
                self.firstPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.firstPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.firstPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.firstPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1
        else:
            if upperChain > 0:
                self.secondPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.secondPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.secondPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.secondPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1

        # search horizontal
        upperChain = 0
        lowerChain = 0
        for offset in xrange(1,5):
            if self.lastMovePlayed[1] - offset < 0:
                break
            if self.board[self.lastMovePlayed[0]][self.lastMovePlayed[1] - offset] == self.currentTurn:
                upperChain += 1
            else:
                break
        for offset in xrange(1,5):
            if self.lastMovePlayed[1] + offset >= self.size:
                break
            if self.board[self.lastMovePlayed[0]][self.lastMovePlayed[1] + offset] == self.currentTurn:
                lowerChain += 1
            else:
                break
        if self.currentTurn == 1:
            if upperChain > 0:
                self.firstPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.firstPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.firstPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.firstPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1
        else:
            if upperChain > 0:
                self.secondPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.secondPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.secondPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.secondPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1

        # search upper left, bottom right diagonal
        upperChain = 0
        lowerChain = 0
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] - offset < 0 or self.lastMovePlayed[1] - offset < 0:
                break
            if self.board[self.lastMovePlayed[0] - offset][self.lastMovePlayed[1] - offset] == self.currentTurn:
                upperChain += 1
            else:
                break
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] + offset >= self.size or  self.lastMovePlayed[1] + offset >= self.size:
                break
            if self.board[self.lastMovePlayed[0] + offset][self.lastMovePlayed[1] + offset] == self.currentTurn:
                lowerChain += 1
            else:
                break
        if self.currentTurn == 1:
            if upperChain > 0:
                self.firstPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.firstPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.firstPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.firstPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1
        else:
            if upperChain > 0:
                self.secondPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.secondPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.secondPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.secondPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1

        # search upper right, bottom left diagonal
        upperChain = 0
        lowerChain = 0
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] - offset < 0 or self.lastMovePlayed[1] + offset >= self.size:
                break
            if self.board[self.lastMovePlayed[0] - offset][self.lastMovePlayed[1] + offset] == self.currentTurn:
                upperChain += 1
            else:
                break
        for offset in xrange(1,5):
            if self.lastMovePlayed[0] + offset >= self.size or self.lastMovePlayed[1] - offset < 0:
                break
            if self.board[self.lastMovePlayed[0] + offset][self.lastMovePlayed[1] - offset] == self.currentTurn:
                lowerChain += 1
            else:
                break
        if self.currentTurn == 1:
            if upperChain > 0:
                self.firstPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.firstPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.firstPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.firstPlayerHeuristic[upperChain + lowerChain] += 1
            else: 
                isolatedCheck += 1
        else:
            if upperChain > 0:
                self.secondPlayerHeuristic[upperChain-1] -= 1
            if lowerChain > 0:
                self.secondPlayerHeuristic[lowerChain-1] -= 1
            if upperChain + lowerChain > 4:
                self.secondPlayerHeuristic[4] += 1
            elif upperChain + lowerChain > 0:
                self.secondPlayerHeuristic[upperChain + lowerChain] += 1
            else:
                isolatedCheck += 1
        #print isolatedCheck
        #print self.currentTurn
        # Account for undercounting
        if isolatedCheck == 4:
            if self.currentTurn == 1:
                self.firstPlayerHeuristic[0] += 1
            else:
                self.secondPlayerHeuristic[0] += 1

        return

    # convert heursitic data to a weighted score
    def calcXinARowScore(self):
        #ADJUSTABLE SCORE WEIGHTINGS
        scoreWeights = [1,5,25,100,999999999]

        p1score = sum([self.firstPlayerHeuristic[i] * scoreWeights[i] for i in range(len(scoreWeights))])
        p2score = sum([self.secondPlayerHeuristic[i] * scoreWeights[i] for i in range(len(scoreWeights))])


        '''TODO: So if you flip this to 1, it'll work for depth 0, else it works for depth 1'''
        
        score = p2score - p1score

        #print "score: " + str(score)
        return score

    # returns a list of tuples, where each tuple is a legal move
    # gives them back order of a spiral starting from the center
    def getLegalActions(self, agentIndex):
        legal_actions = []
        
        spiral = []
        # construct spiral CCW
        start = (int(self.size / 2), int(self.size / 2))
        spiral.append(start)
        side_length = 1

        while spiral[-1] != (0,0):
            f = 1 if side_length % 2 == 1 else -1
            for i in range(side_length):
                spiral.append((spiral[-1][0]+f, spiral[-1][1]))
            for j in range(side_length):
                spiral.append((spiral[-1][0], spiral[-1][1]+f))
            side_length+=1
        for i in range(1, int(self.size)):
            spiral.append((i, 0))

        for row, col in spiral:
            if self.board[row][col] == 0:
                legal_actions.append((row, col))
        return legal_actions

    # returns a list of tuples, where each tuple is a legal move
    # def getLegalActions(self, agentIndex):
    #     legal_actions = []
    #     for row in xrange(self.size):
    #         for col in xrange(self.size):
    #             if self.board[row][col] == 0:
    #                 legal_actions.append((row, col))
    #     return legal_actions

    # returns a new ConnectFiveGameState given an action taken by some agentIndex
    def generateSuccessor(self, agentIndex, action):
        new_board = copy.deepcopy(self.board)
        new_board[action[0]][action[1]] = agentIndex
        successor = ConnectFiveGameState(new_board, agentIndex, 
            copy.deepcopy(self.firstPlayerHeuristic), copy.deepcopy(self.secondPlayerHeuristic),
            action)
        successor.updateXinARowHeuristic()
        successor.currentTurn = -successor.currentTurn

        #print "GENERATESUCCESSOR:  " + str(successor.lastMovePlayed) + "  TURN: " + str(-successor.currentTurn)
        #print successor.firstPlayerHeuristic
        #print successor.secondPlayerHeuristic
        return successor

    # returns a dict with keys being the number in a row and values being how many of those
    # opportunities there are
    def getNumInARow(self):
        return self.firstPlayerHeuristic if self.currentTurn == 1 else self.secondPlayerHeuristic

# minimax agent
class MinimaxAgent:
    def __init__(self, depth=1):
        # fill in stuff here
        self.depth = depth

    # terminal test
    def is_terminal(self, gameState):
        return gameState.isOver()

    def evaluationFunction(self, gameState):
        # come up with a heuristic here to evaluate how good a board is
        return gameState.calcXinARowScore()

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
    minimax_agent = MinimaxAgent(depth=1) #depth = 1
    size = 15
    clean_board = [x[:] for x in [[0]*size]*size]
    clean_board[7][5] = -1
    clean_board[8][6] = -1
    clean_board[9][7] = -1
    
    #print clean_board
    first = {}
    first[0] = 0 
    first[1] = 0
    first[2] = 1
    first[3] = 0
    first[4] = 0
    gameState = ConnectFiveGameState(clean_board, -1, secondPlayerHeuristic=first, lastMovePlayed=(7,7))
    print minimax_agent.getAction(gameState, -1)