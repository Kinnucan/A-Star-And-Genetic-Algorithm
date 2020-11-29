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
            self.ruleString = self.randomRuleset()


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
        print(randElem)
        print(self.ruleString)
        print(self.ruleString[randElem])
        newElem = random.choice(opts)
        newRules = self.ruleString[:randElem] + newElem + self.ruleString[randElem+1:]
        return RulesetState(self.evalFunction, self.maxValue, newRules)

    def getRandomStates(self, n):
        """Builds n random states that use the same eval function and max value but are
        unrelated to this state."""
        newStates = []
        for i in range(n):
            newRule = self.randomRuleset()
            newState = RulesetState(self.evalFunction, self.maxValue, newRule)
            newStates.append(newState)
        return newState

    def randomRuleset(self):
        """Generate a random ruleset string"""
        options = "sflr"  # Leaving out the "arbitrary" random behavior
        rules = ""
        for i in range(self.RULE_LEN):
            rules += random.choice(options)
        return rules

    def crossover(self, otherState):
        """Given another NQueens state, this computes a crossover point and creates
        two new states that have been crossed over."""
        crossPoint = random.randint(0, self.RULE_LEN)
        if crossPoint == 0 or crossPoint == self.RULE_LEN:
            new1 = self.copyState()
            new2 = otherState.copyState()
            return new1, new2
        else:
            newString1 = ""
            newString2 = ""
            newString1 = newString1 + (self.ruleString[:crossPoint])
            newString1 = newString1 + (otherState.ruleString[crossPoint:])
            newString2 = newString2 + (otherState.ruleString[:crossPoint])
            newString2 = newString2 + (self.ruleString[crossPoint:])
            new1 = RulesetState(self.evalFunction, self.maxValue, newString1)
            new2 = RulesetState(self.evalFunction, self.maxValue, newString2)
            print("parent 1 rulestring: " + self.ruleString)
            print("parent 2 rulestring: " + otherState.ruleString)
            print("child 1: " + newString1)
            print("child 2: " + newString2)
            return new1, new2

    def copyState(self):
        """Builds and returns a new state identical to this one"""
        string = self.ruleString
        return RulesetState(self.evalFunction, self.maxValue, string)

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

class GASearcher(object):
    """An algorithm that takes a population of agents, each with a different rulestring, and analyzes their performance
    to determine which rulestrings should be crossed over with one another."""
    def __init__(self, stateGen, popSize=30, maxGenerations=20, crossPerc=0.8, mutePerc=0.01):
        self.best = 0
        self.stateGen = stateGen
        self.popSize = popSize
        self.maxGenerations = maxGenerations
        self.crossPerc = crossPerc
        self.mutePerc = mutePerc
        if self.popSize % 2 == 1:  # if user puts in an odd population size, make it even
            print("Making population size even:")
            self.popSize += 1
        self.currStates = []
        nextState = self.stateGen
        for i in range(self.popSize):
            newState = nextState.copyState()
            self.currStates.append(newState)
            nextState.ruleString = nextState.randomRuleset()
        self.maxFit = self.currStates[0].getMaxValue()
        self.count = 0

    def getCount(self):
        """Returns the current count."""
        return self.count

    def getCurrState(self):
        """Returns the current state."""
        return self.currStates[0]

    def getCurrValue(self):
        """Returns the value currently associated with the current state."""
        return self.currStates[0].getValue()

    # this doesn't seem to ever be run by ALifeGUI
    def run(self):
        status = None
        while self.count < self.maxGenerations:
            status = self.step()

            if status == 'optimal':
                break

    def step(self):
        # keep track of the best state (rulestring)
        overallBest = self.currStates[0]
        # if we've surpsassed the max number of generations, report that we're done
        if self.count > self.maxGenerations:
            return 'local maxima'
        # get the value of each rulestring in the list of current rulestrings
        fits = [state.getValue() for state in self.currStates]
        # if one of those fitnesses is optimal, we have an optimal rulestring in our current list
        if self.maxFit in fits:
            # get the index of the value, which is also the index of the rulestring in fits
            pos = fits.index(self.maxFit)
            # store the optimal rulestring in self.best
            self.best = self.currStates[pos]
            # report having found an optimal value
            return 'optimal'
        else:
            # find the index of the best of the current fitnesses
            bestLoc = fits.index(max(fits))
            # using that index, identify its matching rulestring
            bestOne = self.currStates[bestLoc]
            # create the next pool of parents using the current states and their fitnesses
            parentPool = self.selectParents(self.currStates, fits)
            # update the current states by mating parents in the parent pool
            self.currStates = self.mateParents(parentPool, self.crossPerc, self.mutePerc)
        # update the overall best rulestring
        if bestOne.getValue() > overallBest.getValue():
            overallBest = bestOne
        if verbose:
            print("============== GOAL ==============")
            print("  Last generation best one:")
            print(bestOne)
            print("  Overall best discovered:")
            print(overallBest)
            print("   Number of steps =", self.count)
        # keep track of the best rulestring so far
        self.best = overallBest
        # keep track of how many generations it's been
        # it's possible this is never used by ALifeGUI
        self.count += 1
        # tell the program to run another simulation
        return 'keep going'

    # TODO: Implement the rest of the genetic alg from the localSearch.py file in the Queens folder

    def selectParents(self, states, fitnesses):
        """given a set of states, repeatedly select parents using roulette selection"""
        parents = []
        # once for every state in the states (parents) list...
        for i in range(len(states)):
            print("rulestring: " + states[i].ruleString)
            # select an index based on ratios of fitness
            nextParentPos = self.rouletteSelect(fitnesses)
            # add the parent at the selected index to the list of parents
            parents.append(states[nextParentPos])
        return parents

    def mateParents(self, parents, crossoverPerc, mutationPerc):
        """Given a set of parents, pair them up and cross them together to make
        new kids"""
        newPop = []
        # for every other parent...
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1]
            # randomly decide if the parents will be crossed or not
            doCross = random.random()
            # if so...
            if doCross < crossoverPerc:
                # create two children
                n1, n2 = p1.crossover(p2)
                # add the new children to the population
                newPop.append(n1)
                newPop.append(n2)
            # if not...
            else:
                # create copies of the parents and add them to the population
                newPop.append(p1.copyState())
                newPop.append(p2.copyState())
        # create random mutations in some members of the population
        for i in range(len(newPop)):
            nextOne = newPop[i]
            doMutate = random.random()
            if doMutate <= mutationPerc:
                newPop[i] = nextOne.makeRandomMove()
        return newPop

    def rouletteSelect(self, valueList):
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
        print("roulette select result: " + len(valueList) - 1)
        return len(valueList) - 1
