# CS224W
Final project for CS224W, Network Analysis



Bipartite Graphs:
Nodes: subreddit communities and users
Edges: edges connect user to a subreddit community and the weight is the number of times they have commented in that community


Community Relation Graphs:
Nodes: subreddit communities
Edges: edges connect communities and the weight is the number of common users between the two communities (an user is common if they have commented at least once in both subreddits)


User Comments Graphs:
Nodes: users
Edges: edges connect users and the weight is the number of times the two users have both commented on the same submission (a measurement of how their interests align/do not align)


