

from localSearch import *
from NQueens import NQueens, NQGenerator



def testRandomStarts(alg, reps = 5, sizeList = [4, 8]):
    """Takes in a function name for one of the local search functions, for hill-climbing and simulated annealing. It
     doesn't work for beam search or genetic algorithms. It has optional inputs for a number of repetitions and
     list of sizes to test. """
    allResults = {}
    for siz in sizeList:
        print("testing size", siz)
        allResults[siz] = []
        for rep in range(reps):
            print(".")
            startState = NQueens(siz, full=False)
            result = alg(startState)
            allResults[siz].append(result)
    print("==================================")
    print("Running tests on", alg)
    for siz in sizeList:
        print("---------------")
        print("Size =", siz)
        runs = allResults[siz]
        for i in range(len(runs)):
            (lastVal, maxVal, count) = runs[i]
            print("Run", i+1, ": quality =", lastVal, "out of", maxVal, "count =", count)
            


def testWithStart(alg, state, reps = 5):
    """Run this function only on hill-climbing variants and simulated
    annealing, doesn't work for beam search or GA. Takes in a function name
    for one of the local search functions, and a starting state. It also has
    an optional input a number of repetitions. This runs the given algorithm
    with the specified start state. Can't loop over sizes, but does run reps
    tests and prints the results."""
    runs = []
    for rep in range(reps):
        print(".")
        result = alg(state)
        runs.append(result)
    print("==================================")
    print("Running tests on", alg)
    print(state)
    for i in range(len(runs)):
        (lastVal, maxVal, count) = runs[i]
        print("Run", i+1, ": quality =", lastVal, "out of", maxVal, "count =", count)
            

def testVaryingPops(alg, popSize, reps = 5, sizeList = [4, 8]):
    """Run this on beam search and GA only. Takes in a function name for one
    of the local search functions, and a population size. It
    also has an optional input a number of repetitions. This runs the given
    algorithm with the specified population size. Can't loop over sizes, but does
    run reps tests and prints the results."""
    allResults = {}
    for siz in sizeList:
        print("testing size", siz)
        allResults[siz] = []
        for rep in range(reps):
            print(".")
            result = alg(NQGenerator, popSize)
            allResults[siz].append(result)
    print("==================================")
    print("Running tests on", alg)
    for siz in sizeList:
        print("---------------")
        print("Size =", siz)
        runs = allResults[siz]
        for i in range(len(runs)):
            (lastVal, maxVal, count) = runs[i]
            print("Run", i+1, ": quality =", lastVal, "out of", maxVal, "count =", count)



if __name__ == "__main__":

    testRandomStarts(hillClimb)

    worstState = NQueens(8, [4, 4, 4, 4, 4, 4, 4, 4], full=False)
    testWithStart(stochHillClimb, worstState)

    testVaryingPops(beamSearch, 20)