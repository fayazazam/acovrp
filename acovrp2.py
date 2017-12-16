#!python2

from __future__ import print_function
from tsplibparser import TSPLIBParser
import argparse
import numpy as np
from multiprocessing import Pool

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

	def updatePheromone(self, route, glob = False):
		for x in xrange(0,len(route.customers)-1):
			G.adj[route.customers[x]-1][route.customers[x+1]-1].pher *= (1. - ALPHA)
			if glob:
				G.adj[route.customers[x]-1][route.customers[x+1]-1].pher += ALPHA * (1./route.cost(self))
			else:
				G.adj[route.customers[x]-1][route.customers[x+1]-1].pher += ALPHA * TAU0

	def importance(self, i, j):
		try:
			return self.adj[i][j].pher*np.power((1./self.adj[i][j].dist), BETA)
		except ZeroDivisionError:
			return float('inf')

	def eq1(self, route):
		global dim
		customer = -1
		maxval = 0

		for x in xrange(0,dim): # check every customer
			if x + 1 not in route.customers: # customer has not been visited yet
				tmp = self.importance(route.customers[-1]-1, x)
				if tmp > maxval:
					customer = x + 1
					maxval = tmp
		return customer

	def eq2(self, route):
		global dim
		dart = np.random.rand()
		total = 0 # contains the sum of the importance of all unvisited customers

		for x in xrange(0,dim): # check every customer
			if x + 1 not in route.customers: # customer has not been visited yet
				total += self.importance(route.customers[-1]-1, x)

		sigma = 0
		for x in xrange(0,dim): # check every customer
			if x + 1 not in route.customers: # customer has not been visited yet
				if sigma + self.importance(route.customers[-1]-1, x)/total < dart:
					sigma += self.importance(route.customers[-1]-1, x)/total
					continue
				return x + 1

class Ant(object):
	capacity = 0

	def __init__(self, id):
		self.id = id
		self.route = Route()

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

	def walk(self, G):
		self.route.customers.append(depot) # append to history/route
		self.supply = Ant.capacity # set supply to max capacity

		while len(set(self.route.customers)) < dim: # visit all customers
			self.route.customers.append(self.selectPath(G)) # append new customer to history/route
			if self.route.customers[-1] == depot: # new position is the depot
				self.supply = Ant.capacity # set supply to max capacity
			else: # new position is a customer
				self.supply -= G.V[self.route.customers[-1]-1].demand # subtract customer demand
		self.route.customers.append(depot) # after visiting all customers, return to the depot

		G.updatePheromone(self.route)

class Route(object):
	def __init__(self):
		self.customers = []

	def __str__(self):
		return str(self.customers)

	def cost(self, G):
		c = 0
		for x in xrange(0,len(self.customers)-1):
			c += G.adj[self.customers[x]-1][self.customers[x+1]-1].dist
		return c

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

def walk(ant):
	global G, best

	ant.route.customers.append(depot) # append to history/route
	ant.supply = Ant.capacity # set supply to max capacity

	while len(set(ant.route.customers)) < dim: # visit all customers
		ant.route.customers.append(ant.selectPath(G)) # append new customer to history/route
		if ant.route.customers[-1] == depot: # new position is the depot
			ant.supply = Ant.capacity # set supply to max capacity
		else: # new position is a customer
			ant.supply -= G.V[ant.route.customers[-1]-1].demand # subtract customer demand
	ant.route.customers.append(depot) # after visiting all customers, return to the depot

	G.updatePheromone(ant.route)

	print(ant.route.cost(G))

if __name__ == '__main__':
	global ALPHA, BETA, Q0, M, TAU0, G, best

	parser = argparse.ArgumentParser(description='Use ACO to find solutions for the VRP.')
	parser.add_argument('file', nargs=1, type=str, help='a path to a file in TSPLIB format', metavar='INPUT')
	parser.add_argument('best', nargs=1, type=float, help='a parameter for either the best found solution of the TSPLIB instance', metavar='BEST')
	parser.add_argument('-a', nargs=1, default=[0.1], type=float, required=False, help='a parameter that controls the speed of pheromone evaporation', metavar='ALPHA')
	parser.add_argument('-b', nargs=1, default=[2.3], type=float, required=False, help='a parameter establishing the importance of distance in comparison to pheromone quantity during customer selection', metavar='BETA')
	parser.add_argument('-q', nargs=1, default=[0.9], type=float, required=False, help='a parameter controlling the probability for ants to choose an optimal path over a path determined by proportional selection', metavar='Q0')
	parser.add_argument('-m', nargs=1, default=[25], type=int, required=False, help='a parameter specifying the total number of ants per iteration', metavar='M')
	
	args = parser.parse_args()
	data = TSPLIBParser(args.file.pop()).parse()
	ALPHA = args.a.pop()
	BETA = args.b.pop()
	Q0 = args.q.pop()
	M = args.m.pop()
	TAU0 = 1./args.best.pop()

	G = generateGraphFrom(data)
	best = None # remember the best route

	# Create a list of pre-set length containing the ants
	ants = []
	for i in xrange(0, M):
		ants.append(Ant(i))

	x = 1
	while x < 100:
		p = Pool()
		p.imap_unordered(walk, ants)
		p.close()
		p.join()

		G.updatePheromone(best, True)
		print("iteration "+ str(x) + ", minimal tour length " + str(best.cost(G)), end='\r')
		x += 1