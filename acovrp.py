#!python2

from tsplibparser import TSPLIBParser
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Vertex(object):
	def __init__(self, id):
		self.id = id

class Edge(object):
	def __init__(self, i, j, weight):
		self.arc = (i,j)
		self.weight = weight

class Graph(object):
	def __init__(self):
		self.V = set()
		self.E = set()

def randomGraph(n=20, p=0.3):
	G = Graph()

	for i in xrange(0,n):
		G.V.add(Vertex(i))

	for i in xrange(0,n):
		for j in xrange(i,n):
			if np.random.rand() < p:
				weight = np.random.rand()
				G.E.add(Edge(i,j,weight))

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
	# visualize = True
	# G = randomGraph()
	
	# if visualize:
	# 	drawGraph(G)
	print TSPLIBParser('instances/A/A-n32-k5.vrp').parse()