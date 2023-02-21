import pygame
from vector import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        self.neighbors_costs = {}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+']
        self.pathSymbols = ['.']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.costs = self.get_nodes()

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNodePacMan(self):
        nodes = list(self.nodesLUT.values())
        return nodes[38]

    def getStartTempNodeGhost(self):
        nodes = list(self.nodesLUT.values())
        return nodes[-9]

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)

    #############################
    # returns a list of all nodes in (x,y) format
    def getListOfNodesVector(self):
        return list(self.nodesLUT)

    # returns a node in (x,y) format
    def getVectorFromLUTNode(self, node):
        id = list(self.nodesLUT.values()).index(node)
        listOfVectors = self.getListOfNodesVector()
        return listOfVectors[id]

    # returns neighbors of a node in LUT form
    def getNeighborsObj(self, node):
        node_obj = self.getNodeFromPixels(node[0], node[1])
        return node_obj.neighbors

    # returns neighbors in (x,y) format
    def getNeighbors(self, node):
        neighs_LUT = self.getNeighborsObj(node)
        vals = neighs_LUT.values()
        neighs_LUT2 = []
        for direction in vals:
            if not direction is None:
                neighs_LUT2.append(direction)
        list_neighs = []
        for neigh in neighs_LUT2:
            list_neighs.append(self.getVectorFromLUTNode(neigh))
        return list_neighs

    # used to initialize node system for Dijkstra algorithm
    def get_nodes(self):
        costs_dict = {}
        listOfNodesPixels = self.getListOfNodesVector()
        for node in listOfNodesPixels:
            neigh = self.getNeighborsObj(node)
            temp_neighs = neigh.values()
            temp_list = []
            for direction in temp_neighs:
                if not direction is None:
                    temp_list.append(1)
                else:
                    temp_list.append(None)
            costs_dict[node] = temp_list
        print(costs_dict)
        return costs_dict