import networkx as nx
from networkx.algorithms import bipartite

relevant_subreddits = ['The_Donald', 'PoliticalDiscussion', 'politics', 
						'socialism', 'Libertarian', 'NeutralPolitics',
						'Ask_Politics', 'AskTrumpSupporters', 'moderatepolitics', 
						'democrats', 'Conservative', 'Republican', 
						'Liberal']
files = ['2014-11_bipartite.gml','2015-11_bipartite.gml','2016-11_bipartite.gml']

for path in files:
	print path
	B = nx.Graph()
	G = nx.read_gml(path)
	B.add_nodes_from(relevant_subreddits, bipartite=0)
	nodeList = set([n for n in G.nodes()])
	for reddit in relevant_subreddits:
		if reddit in nodeList:
			nodeList.remove(reddit)
	B.add_nodes_from(list(nodeList), bipartite=1)
	# B.add_edges_from([e for e in G.edges()])
	edgeList = []
	for e in G.edges():
		if e[0] not in relevant_subreddits and e[1] not in relevant_subreddits:
			continue
		edgeList.append(e)
	B.add_edges_from(edgeList)
	# print(bipartite.is_bipartite(B))
	# print(bipartite.average_clustering(B))
	# X, Y = bipartite.sets(B)
	print('Clustering Coefficient')
	print(bipartite.average_clustering(B,list(nodeList)))
	# print(bipartite.average_clustering(B,Y))
	print('Density')
	print(bipartite.density(B,list(nodeList)))

# Toy
# B = nx.Graph()
# Add nodes with the node attribute "bipartite"
# B.add_nodes_from(['e' , 'f', 'g'], bipartite=0)
# B.add_nodes_from(['a', 'b', 'c'], bipartite=1)
# Add edges only between nodes of opposite node sets
# B.add_edges_from([('g', 'a'), ('b', 'f'), ('e', 'c')])
# print(bipartite.is_bipartite(B))