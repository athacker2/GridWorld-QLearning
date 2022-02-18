from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue
import math

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

def dfs(graph,start,goal):
    frontier = LifoQueue()
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

def djikstra(graph,start,goal):
    frontier = PriorityQueue()
    visited = dict()
    prev = dict()
    costs = dict()

    prev[start] = -1
    costs[start] = 0
    frontier.put((0,start))

    while(frontier.qsize() > 0):
        currCost, currNode = frontier.get()
        if(currNode in visited):
            continue
        visited[currNode] = True

        # print("Node: {0}".format(currNode))

        if(currNode == goal):
            print("Found Goal")
            path = []
            while currNode != -1:
                path.append(currNode)
                currNode = prev[currNode]
            path.reverse()
            print(path)
            return

        for node in graph.getActions(currNode):
            if node not in visited and currCost + node[1] < costs.get(node[0],math.inf):
                frontier.put((currCost + node[1],node[0])) 
                prev[node[0]] = currNode
                costs[node[0]] = currCost + node[1]
        
    
    print("No Path to Goal")
    return


