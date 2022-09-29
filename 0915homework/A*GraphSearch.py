from pythonds.graphs import PriorityQueue, Graph, Vertex
from scipy.spatial import distance
import time
import os
import numpy as np
import scipy
from skimage import io
from adjGraph import Graph

class A_Star(Graph):
    def __init__(self):
        super().__init__()
    def buildGraph(self,image):
        print(image)
        print(image.shape)
        self.columns = image.shape[1]
        for row in range(image.shape[0]-1):
            for column in range(image.shape[1]-1):
                name = (image.shape[1] * row) + column
                name_right = (image.shape[1] * row) + (column+1)
                name_down = (image.shape[1] * (row+1)) + column
                weight_right = max(image[row,column] - 50,1) + max(image[row,column+1] - 50, 1)
                weight_down = max(image[row,column]-50,1) + max(image[row+1,column] - 50, 1)
                self.addEdge(name,name_right,weight_right)
                self.addEdge(name_right,name,weight_right)
                self.addEdge(name,name_down,weight_down)
                self.addEdge(name_down,name,weight_down) 
    def distance_between_nodes(self, node1, node2):
        node1_id = node1.id
        node2_id = node2.id
        row1 = int(node1_id/self.columns)
        column1 = node1_id%self.columns
        row2 = int(node2_id/self.columns)
        column2 = node2_id%self.columns
        return distance.euclidean((row1,column1), (row2,column2))
    def dijkstra(self,start):
        pq = PriorityQueue()
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(),v) for v in self])
        while not pq.isEmpty():
            currentVert = pq.delMin()
#             print(currentVert.getId(),currentVert.getDistance())
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert,newDist) 
    def astar(self,start,goal):
        pq = PriorityQueue()
        closed = []
        g_score_dict = {start: 0}
        pq.buildHeap([(self.distance_between_nodes(start,goal),start)])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            closed.append(currentVert)
            if currentVert.id == goal.id:
                break
            for nextVert in currentVert.getConnections():
                tentative_gScore = g_score_dict[currentVert] + currentVert.getWeight(nextVert)                
                if nextVert not in g_score_dict or tentative_gScore < g_score_dict[nextVert]:                    
                    g_score_dict[nextVert] = tentative_gScore
                    fScore = tentative_gScore + self.distance_between_nodes(nextVert,goal)
                    nextVert.setDistance(fScore)
                    nextVert.setPred(currentVert)
                    pq.add((fScore, nextVert))
        return pq, closed
    def traverse(self,y):
        x = y
        pred_path = []
        while (x.getPred()):
            pred_path.append(x.getId())
            x = x.getPred()
        pred_path.append(x.getId())
        return pred_path            

g1 = A_Star()
image = io.imread('retina.png', as_gray=True)
g1.buildGraph(image)
# for v in g:
#     for key in v.connectedTo:
#         print(v.id, key.id)
start_name = (image.shape[1] * 193) + 5
tic = time.time()
g1.dijkstra(g1.getVertex(start_name))
pq, closed = g1.astar(start_name, 0)
toc = time.time()
print("\n Time taken: {} seconds".format(toc-tic))

# set up for picture
x_closed = tuple(int(v.id/image.shape[1]) for v in closed)
y_closed = tuple(v.id%image.shape[1] for v in closed)
# print(x_closed, y_closed)
open_nodes = [i[1] for i in pq.heapArray if i[1] != 0]
x_open = tuple(int(v.id/image.shape[1]) for v in open_nodes)
y_open = tuple(v.id%image.shape[1] for v in open_nodes)
# print(x_open, y_open)

end_name = (image.shape[1] * 14) + 104
pred_path1 = g1.traverse(g1.getVertex(end_name))

rows1 = tuple(int(i/image.shape[1]) for i in pred_path1)
columns1 = tuple(i%image.shape[1] for i in pred_path1)

import matplotlib.pyplot as plt
plt.imshow(image, cmap = 'gray')
plt.show()

#part (a) graph
import matplotlib.pyplot as plt
plt.imshow(image, cmap = 'gray')
plt.plot(columns1,rows1, 'r')
plt.show()