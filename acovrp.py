#!python2

from tsplibparser import TSPLIBParser
import matplotlib.pyplot as plt
from random import randint
import networkx as nx
import numpy as np

class Vertex(object):
	def __init__(self, id):
		self.id = id
		#coordinates?

class Edge(object):
	def __init__(self, i, j, weight):
		self.arc = (i,j)
		self.weight = weight

class Graph(object):
	def __init__(self):
		self.V = set()
		self.E = set()

	def __str__(self):
		return V.id

class Ant(object):
	capacity = 0

	def __init__(self, id):
		self.id = id

def randomGraph(n=20, p=0.25):
	G = Graph()

	for i in xrange(0,n):
		G.V.add(Vertex(i))

	for i in xrange(0,n):
		for j in xrange(i,n):
			#if np.random.rand() < p:
			weight = np.random.rand()
			G.E.add(Edge(i,j,weight))
			G.E.add(Edge(j,i,weight))

	return G

def drawGraph(G):
	NG = nx.Graph()

	# nodes
	labels = {}

	for v in G.V:
		NG.add_node(v.id)
		labels[v.id] = str(v.id)

	# edges
	for e in G.E:
		NG.add_edge(*e.arc, weight=e.weight)

	pos = nx.spring_layout(NG) # positions for all nodes
	nx.draw_networkx_nodes(NG, pos)
	nx.draw_networkx_edges(NG, pos)
	nx.draw_networkx_labels(NG, pos, labels, font_color='w')

	plt.axis('off')
	plt.show()

def walkingAnt(G, depot, i):
	print "Walking"

	currentNode = depot
	nodesSeen = []
	amountDelivered = 0
	route = []

	nodesSeen.append(depot)


	while amountDelivered < Ant.capacity:
		randomNode = randint(0, len(G.V))
		if (randomNode not in nodesSeen and randomNode != currentNode):
			amountDelivered = 5 #value of edge between node i and j
			route.append(randomNode)
			nodesSeen.append(randomNode) 
			currentNode = randomNode
		else:
			break	
	print amountDelivered
	print route



if __name__ == '__main__':
	beta = 2.3
	alpha = 0.1
	numberOfAnts = 2
	Ant.capacity = 100

	visualize = False
	G = randomGraph()
	
	if visualize:
		drawGraph(G)

	#Set one of the nodes in the set as the depot
	depot = randint(0, len(G.V))
	print depot

	#Create a list of pre-set length containing the ants
	ants = []
	for i in xrange(0, numberOfAnts):
		ants.append(Ant(i))

	for i in range(0, len(ants)):
		walkingAnt(G, depot, ants[i])
		print "----next----\n"

	











