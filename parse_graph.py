import networkx as nx

relevant_subreddits = ['The_Donald', 'PoliticalDiscussion', 'politics', 
						'socialism', 'Libertarian', 'NeutralPolitics',
						'Ask_Politics', 'AskTrumpSupporters', 'moderatepolitics', 
						'democrats', 'Conservative', 'Republican', 
						'Liberal']
files = ['2014-11_bipartite.gml', '2015-11_bipartite.gml', '2016-11_bipartite.gml']

def main():
	comment_counts = {}
	N = nx.Graph()
	for path in files:
		# count = 0
		G = nx.read_gml('graphs/' + path)
		for edge in G.edges(data='weight'):
			if 'politics' == edge[0] or 'politics' == edge[1]:
				count += 1
		# print(count)
			print(edge)
			if edge[2] > 5 and ('The_Donald' == edge[0] or 'The_Donald' == edge[1] or 'politics' == edge[0] or 'politics' == edge[1]):
				N.add_node(edge[0])
				N.add_node(edge[1])
				N.add_edge(edge[0],edge[1])
		# G.remove_nodes_from(nx.isolates(G))
	print(nx.number_of_nodes(N))
	print(nx.number_of_edges(N))
	nx.write_gml(N, 'relationsmall2016.gml')

if __name__ == "__main__":
	main()