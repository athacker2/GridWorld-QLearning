import matplotlib
from copy import deepcopy
import argparse

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QGridLayout, QLabel, QSlider)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from GridWorld import QLearnerPlayer, GridSearch, GridWorld
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import random

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.played = False
        self.pathHistory = []
        self.currStep = 0

        self.initUI()


    def initUI(self):
    
        grid = QGridLayout()

        self.figure = Figure()
        self.vis = FigureCanvas(self.figure)

        self.runButton = QPushButton("Run",self)

        self.gammaLabel = QLabel("Gamma",self)
        self.epsilonLabel = QLabel("Epsilon",self)
        self.epsilonDecayLabel = QLabel("Epsilon Decay",self)
        self.minEpsilonLabel = QLabel("Min Epsilon", self)
        self.epochsLabel = QLabel("Epochs",self)
        self.iterationLabel = QLabel("Iteration")
        self.stepLabel = QLabel("Step")

        self.gammaSlider = QSlider(Qt.Orientation.Horizontal,self)
        self.epsilonSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.epsilonDecaySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.minEpsilonSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.epochsSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.iterationSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.stepSlider = QSlider(Qt.Orientation.Horizontal,self)

        grid.addWidget(self.gammaLabel,0,0)
        grid.addWidget(self.gammaSlider,1,0,1,2)
        grid.addWidget(self.epsilonLabel,2,0)
        grid.addWidget(self.epsilonSlider,3,0,1,2)
        grid.addWidget(self.epsilonDecayLabel,4,0)
        grid.addWidget(self.epsilonDecaySlider,5,0,1,2)
        grid.addWidget(self.minEpsilonLabel,6,0)
        grid.addWidget(self.minEpsilonSlider,7,0,1,2)
        grid.addWidget(self.epochsLabel,8,0)
        grid.addWidget(self.epochsSlider,9,0,1,2)
        grid.addWidget(self.runButton,10,0,1,2)

        grid.addWidget(self.stepLabel,10,2)
        grid.addWidget(self.stepSlider,11,2,1,2)

        grid.addWidget(self.vis,0,2,10,10)
        grid.addWidget(self.iterationLabel,12,2)
        grid.addWidget(self.iterationSlider,14,2)

        self.gammaSlider.setValue(50)
        self.epsilonSlider.setValue(99)
        self.minEpsilonSlider.setValue(10)
        self.epsilonDecaySlider.setValue(95)
        self.epochsSlider.setValue(100)

        self.setLayout(grid)
        
        self.connectWidgets()

        self.setWindowTitle("Grid World")
        self.show()
    
    def connectWidgets(self):
        self.runButton.clicked.connect(self.runGridWorld)
        self.iterationSlider.sliderMoved.connect(self.showMap)
        self.stepSlider.sliderMoved.connect(self.showMap)
        self.stepSlider.valueChanged.connect(self.showMap)


    def runGridWorld(self):
        self.played = True
        self.pathHistory = []

        epsilon = self.epsilonSlider.value()/100
        gamma = self.gammaSlider.value()/100
        minEpsilon = self.minEpsilonSlider.value()/100
        epsilonDecay = self.epsilonDecaySlider.value()/100
        epochs = int(self.epochsSlider.value()/100 * 10000)

        agent = QLearnerPlayer(gamma=gamma,epsilon=epsilon,min_epsilon=minEpsilon,epsilon_decay=epsilonDecay)

        self.grid = GridWorld(args.l,args.w)
        self.grid.loadGrid(args.g,args.start,args.goal)
        # self.grid.exampleGrid()

        searchInstance = GridSearch(agent,self.grid)
        self.pathHistory = searchInstance.train(epochs=max(epochs,1))
        
        self.stepSlider.setMinimum(0)
        self.stepSlider.setMaximum(len(self.pathHistory[0]))
        self.stepSlider.setSingleStep(1)

        maxEpochs = int(self.epochsSlider.value()/100 * 10000)
        position = int(maxEpochs*self.iterationSlider.value()/100)

        ax = self.figure.add_subplot(111)
        ax.clear()
        
        ax = self.grid.viewGrid(ax,agentPos=self.pathHistory[position][self.currStep])

        self.vis.draw()
    
    def showMap(self):
        if not self.played:
            print('Play game before using control')
            return
        maxEpochs = int(self.epochsSlider.value()/100 * 10000)
        position = int(maxEpochs*self.iterationSlider.value()/100)

        self.stepSlider.setMinimum(0)
        self.stepSlider.setMaximum(len(self.pathHistory[position])-1)
        step = self.stepSlider.value()

        ax = self.figure.axes[0]
        ax = self.grid.updateGrid(ax,agentPos=self.pathHistory[position][step])
        self.vis.draw()


def launch(filename=None):
    """Launches Main Window"""
    app = QApplication(sys.argv)

    mw = MainWindow()

    sys.exit(app.exec())


'''Pilot'''
parser = argparse.ArgumentParser(description='Get Graph File')
parser.add_argument('-w', default=12, type=int, help='Rows of game')
parser.add_argument('-l', default=6, type=int, help='Columns of game')
parser.add_argument('-g', default='example.txt', type=str, help='Input GridWorld')
parser.add_argument('-goal', default='0,0', type=str, help='Goal Position')
parser.add_argument('-start', default='0,0', type=str, help='Start Position')
args = parser.parse_args()
launch()
