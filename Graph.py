import random
import string

class Graph:

    class Node:
        def __init__(self,id,val):
            self.id = id
            self.val = val
    
    def __init__(self):
        self.counter = 0
        self.Nodes = dict()
        self.Edges = []
    
    def __repr__(self):
        """Print list of nodes and edges in graph"""
        return "Node: {0}\nEdges: {1}".format(self.Nodes,self.Edges)
    
    def generateRandom(self,numNodes,density=0.2,weighted=False):
        """Generates a random graph with a certain number of nodes. Takes input for density of graph (likelihood of edge between two nodes)"""
        assert numNodes > 1

        for i in range(numNodes):
            self.addNode(self.counter)
        
        for i in range(numNodes):
            for j in range(i+1,numNodes):
                if(random.randint(1,10)/10 <= density):
                    self.Edges.append((i,j) if not weighted else (i,j,random.randint(1,10)))                   


    
    def populate(self,nodes,edges):
        """
        Take input for a list of nodes and edges to populate the graph
            nodes: list of tuples specifying nodes of the form: (value, id)
            edges: list of tuples specifying edges of the form: (node1, node2, weight) or (node1, node2)
        """
        for node in nodes:
            assert len(node) == 2
            self.addNode(node[0],node[1])
        for edge in edges:
            assert len(edge) == 2 or len(edge) == 3
            self.addEdge(edge[0],edge[1],None if len(edge) == 2 else edge[2])
    
    def addNode(self, val, id  = None):
        """Take input for a value and id. Create a node with input value and input id (use count as id if none specified)"""
        assert id not in self.Nodes

        if(id is None): # if no id specified, set to current count
            id = self.counter
        self.counter += 1
        
        self.Nodes[id] = val
        return id
    
    def addEdge(self, node1, node2, weight=None):
        """Take input for two nodes and a weight. Add an edge between those two nodes of given weight (or 1 if no weight specified)"""
        assert node1 in self.Nodes and node2 in self.Nodes

        if(weight==None):
            weight = 1
        self.Edges.append((node1,node2,weight))
    
    def getNeighbors(self,node):
        """Returns a list of neighboring nodes for a particular node"""
        neighbors = set()
        for edge in self.Edges:
            if(edge[0] == node):
                neighbors.add(edge[1])
            elif(edge[1] == node):
                neighbors.add(edge[0])
        return list(neighbors)
    
    def getActions(self,node):
        """Returns a list of children nodes and edge costs for a particular node"""
        actions = set()
        for edge in self.Edges:
            if(edge[0] == node):
                actions.add((edge[1],edge[2]))
            elif(edge[1] == node):
                actions.add((edge[0],edge[2]))
        return list(actions)
    