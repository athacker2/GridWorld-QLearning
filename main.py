from Graph import Graph
from SearchAlgos import *
from GridWorld import GridWorld

def main():
    # # test graph from http://www.mathcs.emory.edu/~cheung/Courses/171/Syllabus/11-Graph/bfs.html
    # testGraph = Graph()

    # nodes = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
    # edges = [(0,8),(0,3),(0,1),(1,7),(2,3),(2,7),(2,5),(3,4),(4,8),(5,6)]

    # testGraph.populate(nodes,edges)
    # # bfs(testGraph,0,6)
    # # dfs(testGraph,0,6)

    # djikstraGraph = Graph()

    # nodes = [(0,'A'),(0,'B'),(0,'C'),(0,'D'),(0,'E'),(0,'F')]
    # edges = [('A','B',10),('A','C',15),('B','D',12),('B','F',15),('C','E',10),('D','F',1),('D','E',2),('F','E',5)]
    # djikstraGraph.populate(nodes,edges)

    # # djikstra(djikstraGraph,'A','E')

    # randomGraph = Graph()
    # randomGraph.generateRandom(15,weighted=True,density=0.3,maxWeight=20)
    # djikstra(randomGraph,0,14)
    # randomGraph.viewGraph()

    grid = GridWorld(6,12)
    grid.blockSpace(1,2)
    grid.blockSpace(1,7)
    grid.blockSpace(2,5)
    grid.blockSpace(3,4)
    grid.blockSpace(4,1)
    grid.blockSpace(4,5)
    grid.blockSpace(4,9)

    grid.addReward(0,6,10)
    grid.addReward(1,4,10)
    grid.addReward(2,8,10)
    grid.addReward(1,8,100)
    grid.addReward(3,5,1000)


    grid.viewGrid()
    


if __name__ == "__main__":
    main()