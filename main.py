from Graph import Graph
from SearchAlgos import *

def main():
    testGraph = Graph()

    nodes = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
    edges = [(0,8),(0,3),(0,1),(1,7),(2,3),(2,7),(2,5),(3,4),(4,8),(5,6)]

    testGraph.populate(nodes,edges)
    bfs(testGraph,0,6)


if __name__ == "__main__":
    main()