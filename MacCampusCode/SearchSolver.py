"""  =================================================================
File: SearchSolver.py

This file contains generic definitions for a state space SearchState class,
and a general SearchSolver class.  These classes should be subclassed to make
solvers for a specific problem.
 ==================================================================="""


from FoxQueue import Queue, PriorityQueue
from FoxStack import Stack

# Change this to true to see information about the search as it goes.
verbose = False




class BestFirstSearchSolver(object):
    """This class contains a priority-queue based search algorithm. The Priority-Queue Search can act like
    any best-first search, including UCS and A*, depending on how the "cost" is calculated.  This class contains
    stubs for the helper methods that those algorithms need.  Only the isGoal and generateNeighbors methods
    should be overridden by the subclass.
    These algorithms assume that the qData stored in the states implement the equality operators properly!"""
    
    def __init__(self, taskAdvisor):
        """Creates a Best-First search solver, with the given task advisor. This takes in a "task advisor" and
        sets up the qData needed for the search, the fringe and visited sets, and the counts of
        how many nodes were created and visited.
        The only generic qData are instance variables that count the number of nodes created and the number of
        nodes visited (that corresponds more or less to the number of nodes added to the queue and the number of nodes
        removed from the queue (and not found to be redundant)).  In addition, there are instance variables for the
        search queues for both BFS and PQSearch, so that we can step through the algorithms rather than just running
        them all at once"""
        self.taskAdvisor = taskAdvisor
        self.nodesCreated = 0
        self.nodesVisited = 0
        self.fringe = None
        self.visited = None

    def _initializeCounts(self):
        """A private helper to initialize the counts, since they need to be initialized anew each time the
        search algorithms are called"""
        self.nodesCreated = 0
        self.nodesVisited = 0

    def getNodesCreated(self):
        """Returns the value of self.nodesCreated"""
        return self.nodesCreated

    def getNodesVisited(self):
        """Returns the value of self.nodesVisited"""
        return self.nodesVisited


    def initSearch(self):
        """This method sets up a priority-queue-based search process, initializing the fringe queue, the set of
        visited states, and adding the start state to the fringe queue."""
        self._initializeCounts()
        startState = self.taskAdvisor.getStartState()
        if self.taskAdvisor.isGoal(startState):
            return startState.getPath()
        self.visited = set()
        self.fringe = PriorityQueue()
        self.fringe.insert(startState, startState.getCost())
        self.nodesCreated += 1


    def searchLoop(self):
        """This method runs the search, repeatedly calling for the next step until either
        the search fails and False is returned, or the search completes"""
        while True:
            (nextState, neighbors, isDone) = self.searchStep()
            if nextState == "Fail":
                return False
            elif isDone == "Done":
                # is search is done then nextState actually holds the result
                return nextState
            # Otherwise just do another step of the search


    def searchStep(self):
        """This method performs one step of a priority-queue search. It finds the next node in
        the priority queue, generates its children, and adds the appropriate ones to the priority queue
        It returns three values: the current state, the neighbors of the current state, and a status 
        message.  The message is either "Done", "Fail", or "Not Done" for a normal step."""
        newNeighbors = []
        if self.fringe.isEmpty():
            return (False, False, "Fail")
        nextState, priority = self.fringe.delete()
        if self.taskAdvisor.isGoal(nextState):
            return (nextState, [], "Done")   # when hit goal, neighbors are irrelevant

        # Otherwise, go on
        if verbose:
            print("----------------------")
            print("Current state:", nextState)
        neighbors = self.taskAdvisor.generateNeighbors(nextState)
        self.visited.add(nextState)
        self.nodesVisited += 1

        for n in neighbors:
            visitedMatch = self._hasBeenVisited(n)
            fringeMatch = self._hasBeenFringed(n)

            if (not visitedMatch) and (not fringeMatch):
                if verbose:
                    print("    Neighbor never seen before:", n)
                # this node has not been generated before, add it to the fringe
                self.fringe.insert(n, n.getCost())
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif visitedMatch and visitedMatch.getCost() > n.getCost():
                # if state was visited before but this one is better, add this one to fringe set
                if verbose:
                    print("    Neighbor was already in explored, cost is lower now", n, visitedMatch.getCost(), n.getCost())
                self.fringe.insert(n, n.getCost())
                self.visited.discard(visitedMatch)
                self.visited.add(n)
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif fringeMatch and fringeMatch.getCost() > n.getCost():
                # if state is in fringe but this one is better, add this one to fringe AND
                if verbose:
                    print("    Neighbor state was already in fringe, cost is lower now", n, fringeMatch.getCost(), n.getCost())

                # remove the old one from the fringe
                self.fringe.removeValue(fringeMatch)
                self.fringe.insert(n, n.getCost())
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif visitedMatch:
                if verbose:
                    print("    Neighbor was already in explored, skipping", n)
            elif fringeMatch:
                if verbose:
                    print("    Neighbor was already in fringe, skipping", n)

        # end for
        return nextState, newNeighbors, "Not Done"

    def _hasBeenVisited(self, state):
        """Given a state, it looks through the visited set and seeks a node
        that is "equal" to the input state. It is up to the subclass to
        define what it means for them to be equal. It returns the matching
        state, if any, or False if none"""
        for s in self.visited:
            if s == state:
                return s
        return False

    def _hasBeenFringed(self, state):
        """Given a state, it looks through the fringe set and seeks a node that is "equal" to the
        input state.  It is up to the objects to define what it means for them to be equal.  It
        returns the matching state, if any, or False if none"""
        foundInfo = self.fringe.contains(state)
        if foundInfo:
            return foundInfo
        else:
            return False



class NoCostSearchSolver(object):
    """This class contains a stack or queue search algorithm, so that it can do either BFS or DFS depending on whether
    it is instructed to use a stack or queue. This class contains stubs for the helper methods that those algorithms
    need.  Only the isGoal and generateNeighbors methods should be overridden by the subclass.  BFS is not
    guaranteed to give the best solution on a weighted graph, though it will always give the solution with the least
    edges.  DFS is not guaranteed to give the best solution, ever, but it is more memory-efficient.
    These algorithms assume that the states implement the comparison operators correctly!"""


    def __init__(self, taskAdvisor, mode = 'BFS'):
        """Takes in the task advisor, and an optional mode, which selects DFS or BFS.
        Sets up the qData needed for the search, the fringe and visited sets, and the counts of
        how many nodes were created and visited. The only generic qData are instance variables that count
        the number of nodes created and the number of nodes visited (that corresponds more or less to the
        number of nodes added to the queue and the number of nodes removed from the queue (and not found to be
        redundant))."""
        """This takes in a "task advisor" and sets up the qData needed for the search, the fringe and visited sets, and the counts of
        how many nodes were created and visited.
        The only generic qData are instance variables that count the number of nodes created and the number of
        nodes visited (that corresponds more or less to the number of nodes added to the queue and the number of nodes
        removed from the queue (and not found to be redundant)).  In addition, there are instance variables for the
        search queues for both BFS and PQSearch, so that we can step through the algorithms rather than just running
        them all at once"""
        self.taskAdvisor = taskAdvisor
        self.nodesCreated = 0
        self.nodesVisited = 0
        self.fringe = None
        self.visited = None
        self.mode = mode

    def _initializeCounts(self):
        """A private helper to initialize the counts, since they need to be initialized anew each time the
        search algorithms are called"""
        self.nodesCreated = 0
        self.nodesVisited = 0

    def getNodesCreated(self):
        """Returns the value of self.nodesCreated"""
        return self.nodesCreated

    def getNodesVisited(self):
        """Returns the value of self.nodesVisited"""
        return self.nodesVisited

    def initSearch(self):
        """This method sets up a priority-queue-based search process, initializing the fringe queue, the set of
        visited states, and adding the start state to the fringe queue."""
        self._initializeCounts()
        startState = self.taskAdvisor.getStartState()
        if self.taskAdvisor.isGoal(startState):
            return startState.getPath()
        self.visited = set()
        if self.mode == "BFS":
            self.fringe = Queue()
        else:
            self.fringe = Stack()
        self.fringe.insert(startState)
        self.nodesCreated += 1

    def _setupFringe(self, startState):
        """This method sets up the proper kind of fringe set for this particular search.
        In this case, it creates either a Queue or a Stack, depending on whether we are doing
        BFS or DFS, and it inserts the start state into it."""
        if self.mode == "BFS":
            self.fringe = Queue()
        else:
            self.fringe = Stack()
        self.fringe.insert(startState)

    def searchLoop(self):
        """This method runs the search, repeatedly calling for the next step until either
        the search fails and False is returned, or the search completes"""
        while True:
            (nextState, neighbors, isDone) = self.searchStep()
            if nextState == "Fail":
                return False
            elif isDone == "Done":
                # is search is done then nextState actually holds the result
                return nextState
            # Otherwise just do another step of the search


    def searchStep(self):
        """This method performs one step of a stack or queue search. It finds the next node in
        the stack/queue, generates its children, and adds the appropriate ones to the stack/queue.
        It returns three values: the current state, the neighbors of the current state, and a status
        message.  The message is either "Done", "Fail", or "Not Done" for a normal step."""
        newNeighbors = []
        if self.fringe.isEmpty():
            return (False, False, "Fail")
        nextState = self.fringe.delete()
        if self.taskAdvisor.isGoal(nextState):
            return (nextState, [], "Done")  # when hit goal, neighbors are irrelevant

        # Otherwise, go one
        if verbose:
            print("----------------------")
            print("Current state:", nextState)
        neighbors = self.taskAdvisor.generateNeighbors(nextState)
        self.visited.add(nextState)
        self.nodesVisited += 1

        for n in neighbors:
            visitedMatch = self._hasBeenVisited(n)
            fringeMatch = self._hasBeenFringed(n)

            if (not visitedMatch) and (not fringeMatch):
                if verbose:
                    print("    Neighbor never seen before", n)
                # this node has not been generated before, add it to the fringe
                self.fringe.insert(n)
                newNeighbors.append(n)
                self.nodesCreated += 1
            elif visitedMatch:
                if verbose:
                    print("    Neighbor was already in explored, skipping", n)
            elif fringeMatch:
                if verbose:
                    print("    Neighbor was already in fringe, skipping", n)

        # end for
        return nextState, newNeighbors, "Not Done"

    def _hasBeenVisited(self, state):
        """Given a state, it looks through the visited set and seeks a node
        that is "equal" to the input state. It is up to the state class to
        define what it means for them to be equal. It returns the matching
        state, if any, or False if none"""
        for s in self.visited:
            if s == state:
                return s
        return False

    def _hasBeenFringed(self, state):
        """Given a state, it looks through the fringe set and seeks a node that is "equal" to the
        input state.  It is up to the objects to define what it means for them to be equal.  It
        returns the matching state, if any, or False if none"""
        foundInfo = self.fringe.contains(state)
        if foundInfo:
            return foundInfo
        else:
            return False


