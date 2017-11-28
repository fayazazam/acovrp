#!python2

from tsplibparser import TSPLIBParser
import matplotlib.pyplot as plt
from random import randint
import networkx as nx
import numpy as np

ALPHA = 0.1
BETA = 2.3
Q0 = 0.9
M = 25
TAU0 = 1./784

class Vertex(object):
	def __init__(self, id, x, y):
		self.id = id
		self.coords = (x,y)
		self.demand = 0

class Edge(object):
	def __init__(self, i, j, dist):
		self.arc = (i,j)
		self.dist = dist
		self.pher = TAU0

class Graph(object):
	def __init__(self):
		self.V = []
		self.E = []

	def importance(p, G, i, j):
		return np.power(p*(1./G[i][j]), BETA)

	def eq1(G, history):
		j = -1
		maxval = 0
		for x in xrange(0,len(G.V)): # check every destination
			if x + 1 not in history: # customer has not been visited yet
				tmp = importance(G, history[-1]-1, x)
				if tmp > maxval:
					j = x + 1
					maxval = tmp
		return j

	def eq2(G, pos):


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

	def selectPath(G):
		selected = -1
		if np.random.rand() <= Q0:
			selected = eq1(G, self.route)
		else:
			selected = eq2(G, self.route)

	def routeCost():
		c = 0
		for x in range(0,len(self.route)-1):
			c += G.adj[self.route[x]-1][self.route[x+1]-1].dist
		return c

	def walk(self, G):
		print "Walking"

		self.route.append(depot) # append to history/route
		self.supply = Ant.capacity # set supply to max capacity

		while len(set(self.route)) < dim: # visit all customers
			self.route.append(self.selectPath(G)) # append new customer to history/route
			if self.route[-1] == depot: # new position is the depot
				self.supply = Ant.capacity # set supply to max capacity
			else: # new position is a customer
				self.supply -= G.V[self.route[-1]-1].demand # subtract customer demand
		self.route.append(depot) # after visiting all customers, return to the depot

		print self.route
		print self.cost()		


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
				G.adj[i][j] = Edge(i, j, float('inf'))
			else:
				G.adj[i][j] = Edge(i, j, TSPLIBParser.d_euc2d(G.V[i].coords, G.V[j].coords))
				G.adj[j][i] = Edge(j, i, TSPLIBParser.d_euc2d(G.V[i].coords, G.V[j].coords))

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

if __name__ == '__main__':
	visualize = False
	data = TSPLIBParser('instances/A/A-n32-k5.vrp').parse()
	G = generateGraphFrom(data)
	
	if visualize:
		drawGraph(G)

	# Create a list of pre-set length containing the ants
	ants = []
	for i in xrange(0, M):
		ants.append(Ant(i))

	for ant in ants:
		ant.walk(G)
		# walkingAnt(G, ant)
		print "----next----\n"
		