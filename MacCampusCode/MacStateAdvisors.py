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
        """To print this object, print the row and column in brackets, followed by the
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
        """Create a string for printing that contains the row, col plus path and costs"""
        strng = "Location #" + self.label
        strng += "  " + str(self.pathToMe) + " (" + str(self.costToHere)
        strng += " + " + str(self.costToGoal) + ") = " + str(self.myCost)
        return strng


# ==========================================================================================
# MAZE ADVISORS
# ==========================================================================================

#TODO: Make them.