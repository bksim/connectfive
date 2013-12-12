from ConnectFiveMiniMax import ConnectFiveGameState
from ConnectFiveMiniMax import AlphaBetaAgent
from mpi4py import MPI
import copy
import time


""" A naive parallel AlphaBeta algorithm. Simply splits branches of the minimax tree to
    various processors, and has each one run the serial minimax with alpha-beta pruning
    on each branch.

    args
    gameState: current state of the game to call the method on.
    agentIndex: agentIndex of the player to get the best move for.
    moveOrdering: a move ordering, such as top left to bottom right or spiral.
    comm, p_root: MPI stuff

    The first two arguments are analogous and should be used in the same way as when the
    serial function getAction is called.
"""
def parallelAlphaBeta(gameState, agentIndex, moveOrdering, comm, p_root=0):

    # Get MPI Data
    rank = comm.Get_rank()
    size = comm.Get_size()
    comm.barrier()
    rankTime = time.time()

    # Broadcast info
    gameState = comm.bcast(gameState, root=p_root)
    agentIndex = comm.bcast(agentIndex, root=p_root)
    moveOrdering = comm.bcast(moveOrdering, root=p_root)


    # Get length of moves needed
    numtasks = len(moveOrdering)

    '''HELPFUL PRINT OUT HERE to see if the legal moves are updated'''
    #print numtasks

    # Start and end indices for undivisible sizes
    start = getStart(numtasks, size, rank)
    end = getStart(numtasks, size, rank + 1)

    current_best_score = float("-inf")
    current_best_action = None
    alpha = float("-inf")
    beta = float("inf")

    # CHANGE DEPTH
    agent = AlphaBetaAgent(depth=2)

    # for synchronization of communication
    reduceCounter = 0;

    for action in moveOrdering[start:end]:
        if gameState.board[action[0]][action[1]] != 0:
            continue
        newScore = agent.minValue(gameState.generateSuccessor(agentIndex, action), \
            -agentIndex, agent.depth, alpha, beta)

        alpha = max(alpha, current_best_score)
        
        if reduceCounter < numtasks / size:
            comm.barrier()
            alpha = comm.allreduce(alpha, op=MPI.MAX)
            comm.barrier()
            reduceCounter += 1
        elif reduceCounter == numtasks / size:
            print "rank " + str(rank) + "done"
            reduceCounter += 1
        
        if newScore > current_best_score:
            current_best_score = newScore
            current_best_action = action

        if current_best_score >= beta:
            break;

    move = current_best_action
    score = current_best_score

    # Reduce the partial results to the root process via MaxLoc which is a max or a value 1, paired with a value 2

    maxScore, rankMax = comm.allreduce(score, op=MPI.MAXLOC)

    if rank == p_root:
        if rankMax == p_root:
            maxMove = move
        else:
            maxMove = comm.recv(source=rankMax)
    elif rank == rankMax:
        comm.send(move, dest=p_root)
    comm.barrier()

    print "Rank" + str(rank) + "Time" + str(time.time()-rankTime)

    if rank == p_root:
        #print "move" + str(maxMove)
        #print "score" + str(maxScore)
        return (maxMove, maxScore)
    else:
        return (None, None)

def getStart(numtasks, size, rank):
  # Offset by rank to account for n+1 spaces
  if rank < numtasks % size:
    return (numtasks / size + 1) * rank
  # Offset only by max numtasks % size
  else:
    return numtasks / size * rank + numtasks % size

'''Remove the turn from the list of moves'''
def removeFromSpiral(moveOrdering, turn):
    return [move for move in moveOrdering if move != turn]

if __name__ == '__main__':
    # Get MPI data
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_processors = comm.Get_size()

    if rank == 0:
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

        # reorder the spiral!
        modified_spiral = {}
        for i, action in enumerate(spiral):
            if i % num_processors not in modified_spiral.keys():
                modified_spiral[i % num_processors] = [action]
            else:
                modified_spiral[i % num_processors].append(action)

        mod_spiral = []
        for key in modified_spiral.keys():
            mod_spiral = mod_spiral + modified_spiral[key]

        gameState = ConnectFiveGameState(clean_board, 1, moveOrdering=spiral)

        """SET INITIAL CONDITION HERE """
        gameState = gameState.generateSuccessor(gameState.currentTurn, (6, 6))
        gameState = gameState.generateSuccessor(gameState.currentTurn, (7, 7))
        gameState = gameState.generateSuccessor(gameState.currentTurn, (7, 6))

        print "current turn: " + str(gameState.currentTurn)

        for line in gameState.board:
        	print line

        print "PARALLEL PART STARTS NOW"

        """ START TIMING HERE"""
        timeStart = time.time()
        (ai_move, score) = parallelAlphaBeta(copy.deepcopy(gameState), -1, gameState.moveOrdering, comm, 0)
        print "TIME: " + str(time.time() - timeStart)
        print "AI MOVES: " + str(ai_move)

        gameState.moveOrdering = removeFromSpiral(gameState.moveOrdering, ai_move)
        #boardGraphics = ConnectFiveGraphics(gameState, comm=comm, activateAI=True)
    else:
        parallelAlphaBeta(None, None, None, comm, 0)
