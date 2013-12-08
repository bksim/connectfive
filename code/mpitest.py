from mpi4py import MPI

def parallelEvaluation(moveOrdering, comm, p_root=0):

    # Get MPI Data
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Broadcast board
    moveOrdering = comm.bcast(moveOrdering, root=p_root)

    # Get length of moves needed
    numtasks = len(moveOrdering)

    # Start and end indices for undivisible sizes
    start = getStart(numtasks, size, rank)
    end = getStart(numtasks, size, rank + 1)

    '''TODO: Run the AlphaBeta agent with mymoves to get the best move and its corresponding score'''
    ''' where the move orders per processor are moveOrdering[start:end]'''

    largestMove = 0
    score = 0
    offset = end - start

    for i in xrange(offset):
        if moveOrdering[start+i] > largestMove:
            largestMove = moveOrdering[start+i]
            score = i

    # Reduce the partial results to the root process via MaxLoc which is a max or a value 1, paired with a value 2

    #print "R" + str(rank) + "max" + str(largestMove)

    maxMove, rankMax = comm.allreduce(largestMove, op=MPI.MAXLOC)

    #print "r" + str(rank) + "maxMove" + str(maxMove) + "rankMax" + str(rankMax)

    if rank == p_root:
        if rankMax == p_root:
            maxScore = score
        else:
            maxScore = comm.recv(source=rankMax)
    elif rank == rankMax:
	    comm.send(score, dest=p_root)

    if rank % 2 == 0:
        alpha = 2*rank
        beta = 1/*rank
    else:
        alpha = -2*rank
        beta = -1/rank

    alpha = comm.reduce(alpha, op=MPI.MAX)
    beta = comm.reduce(beta, op=MPI.MIN)

    if rank == p_root:
        return maxMove, maxScore, alpha, beta
    else:
        return None, None

def getStart(numtasks, size, rank):
  # Offset by rank to account for n+1 spaces
  if rank < numtasks % size:
    return (numtasks / size + 1) * rank
  # Offset only by max numtasks % size
  else:
    return numtasks / size * rank + numtasks % size


if __name__ == '__main__':
    print("Welcome to Connect 5!")

    # Get MPI data
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        data = [0,1,2,4,3,5,8,9,7,6]
    else:
		data = None


    [largestData, orderProcessed, alpha, beta] = parallelEvaluation(data, comm, p_root=0)

    if rank == 0:
        print largestData
        print orderProcessed
        print alpha
        print beta
