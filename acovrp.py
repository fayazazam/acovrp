#!python2

from tsplibparser import TSPLIBParser
import matplotlib.pyplot as plt
from random import randint
import networkx as nx
import numpy as np

class Vertex(object):
	def __init__(self, id, x, y):
		self.id = id
		self.coords = (x,y)
		self.demand = 0

class Edge(object):
	def __init__(self, i, j, weight):
		self.arc = (i,j)
		self.weight = weight

class Graph(object):
	def __init__(self):
		self.V = []
		self.E = []

	def shortestPath(self, ant):
		for index in np.argsort(G.adj[ant.pos-1]):
			if index + 1 not in ant.route and ant.supply >= G.V[index].demand:
				return index + 1
			else:
				continue
		return depot

class Ant(object):
	capacity = 0

	def __init__(self, id):
		self.id = id
		self.route = []

	def walk(self, G):
		print "Walking"

		self.pos = depot
		self.route.append(self.pos)
		self.supply = Ant.capacity

		while len(set(self.route)) < dim:
			self.pos = G.shortestPath(self)
			if self.pos == depot:
				self.supply = Ant.capacity
			else:
				self.supply -= G.V[self.pos-1].demand
			self.route.append(self.pos)
		self.route.append(depot)
		print self.route

		length = 0
		for x in range(1,len(self.route)):
			length += G.adj[self.route[x]-2][self.route[x]-1]
		print length

			


# def randomGraph(n=20, p=0.25):
# 	G = Graph()

# 	for i in xrange(0,n):
# 		G.V.add(Vertex(i))

# 	for i in xrange(0,n):
# 		for j in xrange(i,n):
# 			#if np.random.rand() < p:
# 			weight = np.random.rand()
# 			G.E.add(Edge(i,j,weight))
# 			G.E.add(Edge(j,i,weight))

# 	return G

def generateGraphFrom(data):
	global depot, dim

	G = Graph()
	dim = data['dimension']
	depot = data['depot_section'][0]
	Ant.capacity = data['capacity']

	for node in data['node_coord_section']:
		G.V.append(Vertex(node['id'], node['x'], node['y']))

	for node in data['demand_section']:
		G.V[node['id']-1].demand = node['demand']

	G.adj = np.zeros((dim,dim))

	for i in xrange(0,dim):
		for j in xrange(i,dim):
			if i == j:
				G.adj[i][j] = float('inf')
			else:
				G.adj[i][j] = TSPLIBParser.d_euc2d(G.V[i].coords, G.V[j].coords)
				G.adj[j][i] = TSPLIBParser.d_euc2d(G.V[i].coords, G.V[j].coords)

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

def walkingAnt(G, i):
	print "Walking"

	currentNode = depot
	nodesSeen = []
	amountDelivered = 0
	route = []

	nodesSeen.append(depot)

	while amountDelivered < Ant.capacity:
		randomNode = randint(0, len(G.V))
		if (randomNode not in nodesSeen and randomNode != currentNode):
			amountDelivered += 5 #value of edge between node i and j
			route.append(randomNode)
			nodesSeen.append(randomNode) 
			currentNode = randomNode
		else:
			break	
	print amountDelivered
	print route
	print nodesSeen



if __name__ == '__main__':
	beta = 2.3
	alpha = 0.1
	numberOfAnts = 2

	visualize = False
	data = TSPLIBParser('instances/A/A-n32-k5.vrp').parse()
	G = generateGraphFrom(data)
	
	if visualize:
		drawGraph(G)

	# Create a list of pre-set length containing the ants
	ants = []
	for i in xrange(0, numberOfAnts):
		ants.append(Ant(i))

	for ant in ants:
		ant.walk(G)
		# walkingAnt(G, ant)
		print "----next----\n"
		