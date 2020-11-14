"""  =================================================================
File: SearchSolver.py

This file contains generic definitions for a state space SearchState class,
and a general SearchSolver class.  These classes should be subclassed to make
solvers for a specific problem.
 ==================================================================="""

import random
import math


# Change this to true to see information about the search as it goes.
verbose = False


class RulesetState(object):
    """
    This represents a "state" for the local search. Essentially, this packages up a particular rule string with some
    methods to generate neighbor states, and the functionality to call an evaluation function and pass the rule string
    to it to determine the value of a string.
    """

    RULE_LEN = 27

    def __init__(self, evalFunction, maxValue, ruleString=None):
        """Initialize the two basic instance variables to some value"""
        self.evalFunction = evalFunction
        self.maxValue = maxValue
        self.stateValue = None
        if ruleString is not None:
            self.ruleString = ruleString
        else:
            self.ruleString = self._randomRuleset()


    def getValue(self):
        """Access the value of the myCost instance variable"""
        if self.stateValue is None:
            self.stateValue = self.evalFunction(self.ruleString)
        return self.stateValue

    def getMaxValue(self):
        """Return the maximum value this state has been reported to have."""
        return self.maxValue

    def allNeighbors(self):
        """Generates all neighbors of this state. For the ruleset, that means all one-symbol changes."""
        neighbors = []
        for i in range(len(self.ruleString)):
            currSym = self.ruleString[i]
            otherSyms = self._otherSymbols(currSym)
            for c in otherSyms:
                newRule = self.ruleString[:i] + c + self.ruleString[i+1:]
                newState = RulesetState(self.evalFunction, self.maxValue, newRule)
                neighbors.append(newState)
        return neighbors

    def _otherSymbols(self, sym):
        """Given a symbol, return a string of the other symbols besides it."""
        if sym == 'a':
            return 'sflr'
        elif sym == 's':
            return 'aflr'
        elif sym == 'f':
            return 'aslr'
        elif sym == 'l':
            return 'asfr'
        elif sym == 'r':
            return 'asfl'
        else:
            print("_otherSymbols: should never get here!")

    def randomNeighbors(self, num):
        """Generate num random neighbors of this state. Note that the same neighbor could be generated more than once."""
        neighbors = []
        for i in range(num):
            newS = self.makeRandomMove()
            neighbors.append(newS)
        return neighbors

    def makeRandomMove(self):
        """Takes a ruleset and returns a new ruleset identical to the original, but with one random change."""
        randElem = random.randrange(len(self.ruleString))
        opts = self._otherSymbols(self.ruleString[randElem])
        newElem = random.choice(opts)
        newRules = self.ruleString[:randElem] + newElem + self.ruleString[randElem+1:]
        return RulesetState(self.evalFunction, self.maxValue, newRules)

    def getRandomStates(self, n):
        """Builds n random states that use the same eval function and max value but are
        unrelated to this state."""
        newStates = []
        for i in range(n):
            newRule = self._randomRuleset()
            newState = RulesetState(self.evalFunction, self.maxValue, newRule)
            newStates.append(newState)
        return newState

    def _randomRuleset(self):
        """Generate a random ruleset string"""
        options = "sflr"  # Leaving out the "arbitrary" random behavior
        rules = ""
        for i in range(self.RULE_LEN):
            rules += random.choice(options)
        return rules

    def __str__(self):
        """Make a string representation of this state, for printing"""
        return self.ruleString



# ==================================================================
# This section contains an implementation of straightforward
# Hill Climbing. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

class HillClimber(object):
    """Contains the algorithm for hill-climbing and some helper methods."""

    def __init__(self, startState, maxRounds=500):
        """Sets up the starting state"""
        self.startState = startState
        self.maxRounds = maxRounds
        self.maxValue = startState.getMaxValue()
        self.currState = startState
        # This next step is EXPENSIVE!
        self.currValue = self.currState.getValue()
        self.count = 0
        if verbose:
            print("============= START ==============")

    def getCount(self):
        """Returns the current count."""
        return self.count

    def getCurrState(self):
        """Returns the current state."""
        return self.currState

    def getCurrValue(self):
        """Returns the value currently associated with the current state."""
        return self.currValue


    def run(self):
        """Perform the hill-climbing algorithm, starting with the given start state and going until a local maxima is
        found or the maximum rounds is reached"""
        status = None

        while self.currValue < self.maxValue and self.count < self.maxRounds:
            status = self.step()

            if status == 'optimal' or status == 'local maxima':
                break

        if verbose:
            print("============== FINAL STATE ==============")
            print(self.currState)
            print("   Number of steps =", self.count)
            if status == 'optimal':
                print("  FOUND PERFECT SOLUTION")
        return self.currValue, self.maxValue, self.count


    def step(self):
        """Runs one step of hill-climbing, generates children and picks the best one, returning it as its value. Also returns
        a second value that tells if the best child is optimal or not."""
        self.count += 1
        if verbose:
            print("--------- Count =", self.count, "---------")
            print(self.currState)
        neighs = self.currState.randomNeighbors(8)    # TODO: Modify the number of neighbors here
        bestNeigh = self.findBestNeighbor(neighs)
        nextValue = bestNeigh.getValue()
        self.currState = bestNeigh
        self.currValue = nextValue
        if nextValue == self.maxValue:
            return 'optimal'
        if nextValue >= self.currValue:
            if verbose:
                print("Best neighbor:")
                print(bestNeigh)
            return 'keep going'
        else:
            # best is worse than current
            return 'local maxima'


    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value. If there are multiple neighbors with the same best value,
        a random one is chosen"""
        startBest = neighbors[0]
        print(startBest.ruleString)
        bestValue = startBest.getValue()
        bestNeighs = [startBest]
        for neigh in neighbors[1:]:
            value = neigh.getValue()
            if value > bestValue:
                bestNeighs = [neigh]
                bestValue = value
            elif value == bestValue:
                bestNeighs.append(neigh)
        bestNeigh = random.choice(bestNeighs)
        return bestNeigh




# TODO: Implement the Genetic Algorithm searcher modeled on the HillClimber above

class GASearcher(object):

    def __init__(self, stateGen, popSize=30, maxGenerations=2000, crossPerc=0.8, mutePerc=0.01):
        self.stateGen = stateGen

    # TODO: Implement the rest of the genetic alg from the localSearch.py file in the Queens folder

    def selectParents(states, fitnesses):
        """given a set of states, repeatedly select parents using roulette selection"""
        parents = []
        for i in range(len(states)):
            nextParentPos = rouletteSelect(fitnesses)
            parents.append(states[nextParentPos])
        return parents

    def mateParents(parents, crossoverPerc, mutationPerc):
        """Given a set of parents, pair them up and cross them together to make
        new kids"""
        newPop = []
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1]
            doCross = random.random()
            if doCross < crossoverPerc:
                n1, n2 = p1.crossover(p2)
                newPop.append(n1)
                newPop.append(n2)
            else:
                newPop.append(p1.copyState())
                newPop.append(p2.copyState())
        for i in range(len(newPop)):
            nextOne = newPop[i]
            doMutate = random.random()
            if doMutate <= mutationPerc:
                newPop[i] = nextOne.makeRandomMove()
        return newPop

    def rouletteSelect(valueList):
        """takes in a list giving the values for a set of entities.  It randomly
    selects one of the positions in the list by treating the values as a kind of
    probability distribution and sampling from that distribution.  Each entity gets
    a piece of a roulette wheel whose size is based on comparative value: high-value
    entities have the highest probability of being selected, but low-value entities have
    *some* probability of being selected."""
        totalValues = sum(valueList)
        pick = random.random() * totalValues
        s = 0
        for i in range(len(valueList)):
            s += valueList[i]
            if s >= pick:
                return i
        return len(valueList) - 1