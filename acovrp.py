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
		self.adj = []

	def importance(self, i, j):
		return np.power(self.adj[i][j].pher*(1./self.adj[i][j].dist), BETA)

	def eq1(self, hist):
		global dim
		customer = -1
		maxval = 0

		for x in xrange(0,dim): # check every customer
			if x + 1 not in hist: # customer has not been visited yet
				tmp = self.importance(hist[-1]-1, x)
				if tmp > maxval:
					customer = x + 1
					maxval = tmp
		return customer

	def eq2(self, hist):
		global dim
		dart = np.random.rand()
		total = 0 # contains the sum of the importance of all unvisited customers

		for x in xrange(0,dim): # check every customer
			if x + 1 not in hist: # customer has not been visited yet
				total += self.importance(hist[-1]-1, x)

		sigma = 0
		for x in xrange(0,dim): # check every customer
			if x + 1 not in hist: # customer has not been visited yet
				if sigma + self.importance(hist[-1]-1, x)/total < dart:
					sigma += self.importance(hist[-1]-1, x)/total
					continue
				return x + 1

class Ant(object):
	capacity = 0

	def __init__(self, id):
		self.id = id
		self.route = []

	def selectPath(self, G):
		global depot
		selected = -1

		if np.random.rand() <= Q0:
			selected = G.eq1(self.route)
		else:
			selected = G.eq2(self.route)

		if G.V[selected-1].demand > self.supply:
			return depot

		return selected

	def routeCost(self):
		c = 0
		for x in range(0,len(self.route)-1):
			c += G.adj[self.route[x]-1][self.route[x+1]-1].dist
		return c

	def walk(self, G):
		self.route.append(depot) # append to history/route
		self.supply = Ant.capacity # set supply to max capacity

		while len(set(self.route)) < dim: # visit all customers
			self.route.append(self.selectPath(G)) # append new customer to history/route
			if self.route[-1] == depot: # new position is the depot
				self.supply = Ant.capacity # set supply to max capacity
			else: # new position is a customer
				self.supply -= G.V[self.route[-1]-1].demand # subtract customer demand
		self.route.append(depot) # after visiting all customers, return to the depot

		print "Ant", self.id, "route:", self.route
		print "Route cost:", self.routeCost()


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

	for i in xrange(0,dim):
		tmp = []
		for j in xrange(0,dim):
			tmp.append(None)
		G.adj.append(tmp)

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
		