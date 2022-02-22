from copy import deepcopy
from Graph import Graph
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random

class GridWorld(Graph):
    def __init__(self,rows,cols,start=None,end=None):
        """Creates a graph of dimension rows x cols that represents a grid. Adds corresponding edges and nodes. Edges in 4 cardinal directions"""
        super().__init__()

        # seed start and end to corners if not passed in
        if(start == None):
            self.start = (0,0)
        if(end == None):
            self.end = (rows-1,cols-1)

        self.rows = rows
        self.cols = cols
        self.blockSpaces = []
        self.rewards = dict()

        for i in range(rows):
            for j in range(cols):
                self.addNode(0)
        
        for i in range(rows):
            for j in range(cols):
                node1 = i * cols + j
                if not(j == cols-1): # right edge
                    node2 = node1 + 1
                    self.addEdge(node1,node2)
                if not(i == rows-1): # down edge
                    node2 = node1 + cols
                    self.addEdge(node1,node2)
        
    def addReward(self,row,col,val):
        self.rewards[row * self.cols + col] = val
        self.Nodes[row * self.cols + col] = val
    
    def getReward(self,row,col):
        reward = self.rewards.get(row * self.cols + col,-1)

        # clear reward once it has been claimed once,
        if not (reward == -1):
            self.rewards[row * self.cols + col] = -1
        return reward
    
    def blockSpace(self,row,col):
        self.blockSpaces.append((row,col))
        self.removeNodeEdges(row * self.cols + col)
    
    def getNeighbors(self, state):
        node = state[0] * self.cols + state[1]
        neighbors = super().getNeighbors(node)
        neighbors = [(val // self.cols,val % self.cols) for val in neighbors]
        return neighbors
    
    def exampleGrid(self):
        self.blockSpace(1,2)
        self.blockSpace(1,7)
        self.blockSpace(2,5)
        self.blockSpace(3,4)
        self.blockSpace(4,1)
        self.blockSpace(4,5)
        self.blockSpace(4,9)

        self.addReward(0,6,10)
        self.addReward(1,4,10)
        self.addReward(2,8,10)
        self.addReward(1,8,100)
        self.addReward(3,5,1000)

        # set start and goal states
        self.start = (3,1)
        self.goal = (1,8)
    
    def viewGrid(self):
        # resize data
        data = np.array([el[1] for el in self.Nodes.items()])
        data = np.resize(data,(self.rows,self.cols))
        
        # update data for block types for coloring
        for space in self.blockSpaces:
            data[space[0]][space[1]] = 1

        data = np.where(data == 10, 2, data)
        data = np.where(data == 100, 3, data)
        data = np.where(data == 1000, 4, data)


        print(data)

        # create discrete colormap
        cmap = colors.ListedColormap(['pink','grey','blue','yellow','green'])

        fig, ax = plt.subplots()
        ax.imshow(data, cmap=cmap, interpolation ='nearest',
                                alpha = 1, origin='upper', extent=(0,self.cols,self.rows,0))

        # draw gridlines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(0, self.cols, 1))
        ax.set_yticks(np.arange(0, self.rows, 1))

        # drawing path
        # line = plt.Line2D([1.5,2.5],[3.5,3.5],linewidth=1,linestyle='-',color='black')
        # ax.add_line(line)
        plt.show()

class QLearnerPlayer:
    def __init__(self,gamma=0.9,cutoff = 50,epsilon=1,min_epsilon=0.05,epsilon_decay=0.999):  
        # each entry corresponds to a pair of nodes on the board(row,col) 
        self.QTable = dict()
        self.gamma = gamma
        self.cutoff = cutoff
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay

    def getAction(self,currState,actions):
        state_actions = [(currState,action) for action in actions]

        if(random.random() <= self.epsilon):
            return random.choice(state_actions)[1]

        bestMove = ((-1,-1),-1 * math.inf)
        for pair in state_actions:
            if not (pair in self.QTable):
                self.QTable[pair] = 0

            if(self.QTable[pair] > bestMove[1]):
                bestMove = (pair[1],self.QTable[pair])

        return bestMove[0]
    
    def updateQTable(self,currState,nextState,reward,grid):
        futureActions = [(nextState,neighbor) for neighbor in grid.getNeighbors(nextState)]

        maxQ = -1 * math.inf
        for action in futureActions:
            maxQ = max(maxQ,self.QTable.get(action,0))
            
        self.QTable[(currState,nextState)] = reward + self.gamma * maxQ
    
    def updateParams(self):
        self.epsilon = max(self.epsilon*self.epsilon_decay,self.min_epsilon)
         
class GridSearch:
    """Class representing the act of searching a given graph by a given agent"""
    def __init__(self,agent,graph):
        self.graph = graph
        self.agent = agent
    
    def search(self,agent,graph):
        """Search function that starts at the graph's start position and iteratively explores the environment using the agent's search function until a goal state is reached or the search is terminated."""
        
        # for now require each graph instance to have a specified start and goal state(s)
        assert not graph.start == None
        assert not graph.goal == None

        currState = graph.start
        currReward = 0
        currSteps = 0
        while (not currState == graph.goal) and (currSteps < agent.cutoff):
            print("{0}: {1}".format(currSteps,currState))

            # agent decides nextstate based on current state and list of actions
            nextState = agent.getAction(currState,graph.getNeighbors(currState))
            # get reward (currently based only on next state, not (state,action) )
            reward = graph.getReward(nextState[0],nextState[1])
            currReward += reward

            agent.updateQTable(currState,nextState,reward,graph)
            # update step count
            currSteps += 1
            currState = nextState

        
    def train(self,epochs=50):
        for i in range(epochs):
            print("Episode {0}:".format(i))
            self.search(self.agent,deepcopy(self.graph))
            self.agent.updateParams()
        print(self.agent.QTable)

            
