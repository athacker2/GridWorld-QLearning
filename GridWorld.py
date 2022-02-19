from Graph import Graph
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

class GridWorld(Graph):
    def __init__(self,rows,cols):
        """Creates a graph of dimension rows x cols that represents a grid. Adds corresponding edges and nodes. Edges in 4 cardinal directions"""
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.blockSpaces = []
        self.rewards = []

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
        self.rewards.append((row,col,val))
        self.Nodes[row * self.cols + col] = val
    
    def blockSpace(self,row,col):
        self.blockSpaces.append((row,col))
        self.removeNodeEdges(row * self.cols + col)
    
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

        data[3,1] = -1

        print(data)

        # create discrete colormap
        cmap = colors.ListedColormap(['white','pink','grey','blue','yellow','green'])

        fig, ax = plt.subplots()
        ax.imshow(data, cmap=cmap, interpolation ='nearest',
                                alpha = 1, origin='upper', extent=(0,self.cols,self.rows,0))

        # draw gridlines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(0, self.cols, 1))
        ax.set_yticks(np.arange(0, self.rows, 1))

        # drawing path
        # line = plt.Line2D([1.5,2.5],[3.5,3.5],linewidth=1,linestyle='-',color='black')
        ax.add_line(line)
        plt.show()



                
        