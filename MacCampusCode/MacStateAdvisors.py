# ==========================================================================================
# MAZE STATES
# ==========================================================================================

class MacState(object):
    """This represents the state of a search on a graph.  It does not
    represent the entire graph, just the current location or vertex within the graph, and the
    series of vertices that have been traversed to get to this location.  That
    is represented in the pathToMe instance variable inherited from the parent
    class.  The cost is determined externally, by the task advisor.
    NOTE: for many search algorithms, we need to store the state object in a set, and to be able to find equivalent
    states that may have different costs, but fundamentally refer to the same place in the map.
    Thus any state class you create MUST implement the __eq__ and __hash__ methods, which are used by Python's set
    data type. These methods should be based on the information about the location in the map. For this
    state, that means the row and column indices of the grid square this state represents."""

    def __init__(self, label, path=None, cost=None):
        """Given the numerical label of the location of the current state, and optional path
        and cost, initializes the state for the search"""
        if path is None:
            self.pathToMe = []
        else:
            self.pathToMe = path
        self.myCost = cost
        self.label = label

    def setPath(self, newPath):
        """This is a method that Dijkstra's needs."""
        self.pathToMe = newPath

    def getPath(self):
        """Access the value of the pathToMe instance variable"""
        return self.pathToMe

    def getCost(self):
        """Access the value of the myCost instance variable"""
        return self.myCost

    def getLocation(self):
        """Return the numerical vertex label of the location of this state"""
        return self.label

    def __eq__(self, state):
        """Check if the input is the same type, and if it represents the same location/vertex
        Overloads the == operator."""
        if type(state) is type(self):
            return state.label == self.label
        else:
            return False

    def __hash__(self):
        """Makes the state hashable by hashing its label, so that it can be stored in
        a set or dictionary. Note that states that are == will produce the same hash value."""
        return hash(self.label)

    def __str__(self):
        """To print this object, print the location number, followed by the
        path and cost"""
        strng = "Location #" + self.label
        strng += "  " + str(self.pathToMe) + " " + str(self.myCost)
        return strng



class AStarMacState(MacState):
    """This represents the state of a search on a graph.  It does not
represent the graph, just the current location or vertex in the maze, and the
series of vertices that have been traversed to get to this location.  That
is represented in the pathToMe instance variable inherited from the parent
class.  The cost is determined externally."""

    def __init__(self, label, path=None, costToHere=None, costToGoal=None):
        """Given the row and column, the current path, and the two costs (cost so far and heuristic
        cost to come, this creates a state/node for the search"""

        MacState.__init__(self, label, path, costToHere + costToGoal)
        self.costToHere = costToHere
        self.costToGoal = costToGoal
        self.myCost = self.costToHere + self.costToGoal

    def getCostToHere(self):
        """Return the cost so far"""
        return self.costToHere

    def getCostToGoal(self):
        """Return the heuristic estimate cost to the goal"""
        return self.costToGoal

    def __str__(self):
        """Create a string for printing that contains the location number plus path and costs"""
        strng = "Location #" + self.label
        strng += "  " + str(self.pathToMe) + " (" + str(self.costToHere)
        strng += " + " + str(self.costToGoal) + ") = " + str(self.myCost)
        return strng


# ==========================================================================================
# MAZE ADVISORS
# ==========================================================================================

class MacTaskAdvisor(object):
    """This is the task advisor for the graph navigation task in general. it knows how to determine what a goal
    is, and how to work with the MacState, and how to generate neighbors in general. There will be
    subclasses of this class for each kind of search, because the details of costs for neighbors vary from
    one algorithm to the next."""

    def __init__(self, macMap, startLabel, goalLabel):
        """Given a map of a graph, the starting and goal locations, this initializes the variables
        that hold details of the problem"""
        self.mac = macMap
        self.goal = goalLabel
        self.startState = self._setupInitialState(startLabel)

    def _setupInitialState(self, startLabel):
        """This creates and returns a proper start state for this particular
        class. In this case cost is the distance travelled so far, and that
        starts at whatever the starting position has in it."""
        return MacState(startLabel, [])

    def getStartState(self):
        """Returns the start state, in the proper form to be used by the search."""
        return self.startState


    def isGoal(self, state):
        """Given a state, check if it is a goal state.  It must have the same label
        as the goal"""
        vertex = state.getLocation()
        if vertex == self.goal:
            return True
        else:
            return False

    def generateNeighbors(self, state):
        """Given a state, determine all legal neighbors, and generates the resulting state for each legal move.
        It returns a list of these neighbor states."""
        vertex = state.getLocation()
        rawNeighs = self.mac.getNeighbors(vertex)
        neighs = []
        for neighLabel in rawNeighs:
            neighs.append(self._buildNeighborState(state, neighLabel))
        return neighs

    def _buildNeighborState(self, currState, neighLabel):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        This will be overridden by most subclasses!"""
        currLabel = currState.getLocation()
        newPath = currState.getPath()[:]
        newPath.append(currLabel)
        return MacState(neighLabel, newPath)


class UCSMacAdvisor(MacTaskAdvisor):
    """This class is a subclass of the MacTaskAdvisor. It implements the cost calculations
    used for UCS search, and is intended to be paired with a BestFirstSearchSolver."""

    def _setupInitialState(self, startLabel):
        """This creates and returns a proper start state for this particular
        class. In this case cost is the distance travelled so far, and that
        starts at whatever the starting position has in it."""
        return MacState(startLabel, [], 0)

    def _buildNeighborState(self, currState, neighLabel):
        """Given the current state and the location of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        In this case, the cost is the cost in currState plus the cost in the neighbor."""
        currLabel = currState.getLocation()
        newPath = currState.getPath()[:]
        newPath.append(currLabel)
        oldCost = currState.getCost()
        newCost = self.mac.getWeight(currLabel, neighLabel)
        return MacState(neighLabel, newPath, oldCost + newCost)


class AStarMacAdvisor(MacTaskAdvisor):
    """This class is a subclass of the MacTaskAdvisor. It implements the cost calculations
    used for A* search, using the AStarState, which maintains both g and h costs. It is intended to
    be paired with a BestFirstSearchSolver."""

    def _setupInitialState(self, startLabel):
        """This creates and returns a proper start state for this particular
        class. In this case, it computes all the two values, g, and h:
        g = the cost of the path from the starting location to the starting location (i.e., 0)
        h = the heuristic distance from the starting location to the goal
        The f cost is automatically computed by the AStarMazeState (f = g + h)
        """
        g = 0
        h = self._calcDistToGoal(startLabel)
        return AStarMacState(startLabel, [], g, h)

    def _buildNeighborState(self, currState, neighLabel):
        """Given the current state and the location number of the neighbor, this builds
        a new state, computing the cost as appropriate for the class.
        In this case, we need to update both g and h costs for the new state:
        new g = old g + new edge's weight,
        new h = distance to goal of new vertex"""
        currLabel = currState.getLocation()
        newPath = currState.getPath()[:]
        newPath.append(currLabel)
        newG = currState.getCostToHere() + self.mac.getWeight(currLabel, neighLabel)
        newH = self._calcDistToGoal(neighLabel)
        return AStarMacState(neighLabel, newPath, newG, newH)

    def _calcDistToGoal(self, vertexLabel):
        """Compute the distance to the goal using the standard Euclidean metric.  Compute
        the difference in x values and in y values, square each one, add them up, and take the square root"""
        return self.mac.heuristicDistance(vertexLabel, self.goal)