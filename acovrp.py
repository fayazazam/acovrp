#!python2

import matplotlib.pyplot as plt
import networkx as nx

if __name__ == '__main__':
	visualize = True
	G = nx.fast_gnp_random_graph(10, 0.2, 42, True)
	print nx.all_pairs_node_connectivity(G)
	if visualize:
		nx.draw_shell(G)
		plt.show()