
import MapGraph


     
# newOlin = MapGraph.readMapFile("olinGraph.txt")
# print("Read in Olin graph")



macGraph = MapGraph.readMapFile("macGraph.txt")
print("Read in Macalester graph")

print("Neighbors of node 85:")
print(macGraph.getNeighbors(85))
print("Straight-line distance between 85 and 86:", macGraph.heuristicDist(85, 86))
print("Straight-line distance between 85 and 12:", macGraph.heuristicDist(85, 12))
