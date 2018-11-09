import networkx as nx
from networkx.algorithms import bipartite
import random

relevant_subreddits = ['The_Donald', 'PoliticalDiscussion', 'politics', 
						'socialism', 'Libertarian', 'NeutralPolitics',
						'Ask_Politics', 'AskTrumpSupporters', 'moderatepolitics', 
						'democrats', 'Conservative', 'Republican', 
						'Liberal']
files = ['2014-11_bipartite.gml','2015-11_bipartite.gml','2016-11_bipartite.gml']

def main():
	for path in files:
		print(path)
		B = nx.Graph()
		G = nx.read_gml('graphs/' + path)
		B.add_nodes_from(relevant_subreddits, bipartite=0)
		nodeList = set([n for n in G.nodes()])
		for reddit in relevant_subreddits:
			if reddit in nodeList:
				nodeList.remove(reddit)
		B.add_nodes_from(list(nodeList), bipartite=1)
		# print(nx.number_of_nodes(G))
		# B.add_edges_from([e for e in G.edges()])
		edgeList = []
		for e in G.edges():
			if e[0] not in relevant_subreddits and e[1] not in relevant_subreddits:
				continue
			edgeList.append(e)
		B.add_edges_from(edgeList)
		# print(nx.number_of_edges(G))
		# print(bipartite.is_bipartite(B))
		# print(bipartite.average_clustering(B))

		result = random.sample(list(nodeList), 500)

		print('Clustering Coefficient')
		print(bipartite.average_clustering(B,result))
		print('Density')
		print(bipartite.density(B,result))

if __name__ == "__main__":
	main()