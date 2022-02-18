from Graph import Graph
from SearchAlgos import *

def main():
    # test graph from http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/11-Graph/bfs.html
    testGraph = Graph()

    nodes = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
    edges = [(0,8),(0,3),(0,1),(1,7),(2,3),(2,7),(2,5),(3,4),(4,8),(5,6)]

    testGraph.populate(nodes,edges)
    # bfs(testGraph,0,6)
    # dfs(testGraph,0,6)

    djikstraGraph = Graph()

    nodes = [(0,'A'),(0,'B'),(0,'C'),(0,'D'),(0,'E'),(0,'F')]
    edges = [('A','B',10),('A','C',15),('B','D',12),('B','F',15),('C','E',10),('D','F',1),('D','E',2),('F','E',5)]
    djikstraGraph.populate(nodes,edges)

    # djikstra(djikstraGraph,'A','E')

    randomGraph = Graph()
    randomGraph.generateRandom(10,weighted=True,density=0.5)
    djikstra(randomGraph,0,4)
    randomGraph.viewGraph()


if __name__ == "__main__":
    main()