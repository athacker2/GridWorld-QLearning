from queue import PriorityQueue
from queue import Queue

def bfs(graph, start, goal):
    frontier = Queue()
    visited = dict()
    frontier.put(start)

    while(frontier.qsize() > 0):
        currNode = frontier.get()
        if(currNode in visited): 
            continue

        print("Node: {0}".format(currNode))

        for node in graph.getNeighbors(currNode):
            if(node == goal):
                print("Found Goal")
                return
            if node not in visited:
                frontier.put(node)
        
        visited[currNode] = True
    
    print("No Path to Goal")
    return
