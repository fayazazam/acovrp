#!python2

from random import randint
import numpy as np

class graph():
	def __init__(self):
		self.n = randint(2,10) # number of nodes
		self.a = randint(1,(self.n*(self.n-1)/2)); # number of edges
		self.matrix = np.empty((self.n, self.n))
		rand = 8
		for i in xrange(0, self.n):
			for j in xrange(0, self.n):
				if i != j:
					if rand > randint(0,rand):
						weight = randint(1,self.n)
						self.matrix[i][j] = weight
						self.matrix[j][i] = weight
					else:
						self.matrix[i][j] = -1
						self.matrix[j][i] = -1
				else:
					self.matrix[i][j] = -1
					self.matrix[j][i] = -1
		print self.matrix

class customer():
	def __init__(self, demand):
		self.demand = demand

class ant():
	def __init__(self):
		self.current = 0
		self.next = 0
		self.capacity = 10
		self.distance = 0

if __name__=='__main__':
	G = graph()