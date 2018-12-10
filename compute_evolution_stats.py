import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import time

years = {"2016":12}

def plot(y, metric):
    ticks = range(1, sum(years.values())+1)
    months = [i*2 for i in range(1,7)]
    year = years.keys()[0]
    labels = [str(month)+"/"+year for month in months]
    print(labels)

    fig = plt.figure()
    plt.plot(months,y)
    plt.xticks(months, labels, rotation=45)
    plt.xlabel("Time (month/year)")
    plt.ylabel(metric)
    plt.title(metric+" (2016)")
    plt.savefig(metric)
    plt.show()

def main():
    directory = "NewUserGraphEdgeLists/"
    avg_degrees = []
    cs = []
    ccs = []
    densities = []
    edges = []

    for year in years.keys():
        months = [str(i*2) for i in range(1,7)]
        
        for i in range(len(months)):
            month = int(months[i])
            if month < 10 and month%2 == 0:
                months[i] = "0"+months[i]
        print(months)
        
        for month in months:
            print(month)
            filename = directory + year + "-" + month + "_user_comments.gml"
            
            a = time.time()
            print("Reading in graph")
            G = nx.read_gml(filename)
            b = time.time()
            print("Finished reading in graph")
            print(b-a)
            
            print("Isolating graph")
            isolated = nx.isolates(G)
            G.remove_nodes_from(isolated)
            print("Done isolating graph")
            c = time.time()
            print(c-b)
            print("Isolated: {0}".format(len(isolated)))
            
            print("Writing filtered graph")
            nx.write_gml(G, "usergraph_filtered"+month+"-"+year+".gml")
            print("Finished writing filtered graph")
            d = time.time()
            print(d-c)

            print("Average degrees")
            avg_degree = np.mean(G.degree().values())
            #avg_degree = nx.average_neighbor_degree(G, nodes=random_sample, weight="weight")
            avg_degrees.append(avg_degree)
            print("Finished finding average degrees")
            g = time.time()
            print(g-d)
            print("avg degrees")
            print(avg_degrees)

            print("Clustering coefficient")
            #random_sample = random.sample(G.nodes(), 100)
            cs.append(nx.average_clustering(G))
            e = time.time()
            print("Finished finding clustering coefficients")
            print(e-g)
            print("clustering coefficients")
            print(cs)

            print("Connected components")
            ccs.append(nx.number_connected_components(G))
            print("Finished finding connected components")
            f = time.time()
            print(f-e)
            print("connected components")
            print(ccs)

            print("Densities")
            densities.append(nx.density(G))
            h = time.time()
            print("Finished finding densities")
            print(h-g)
            print("densities")
            print(densities)
            
            print("Edges")
            edges.append(G.number_of_edges())
            k = time.time()
            print("Finished finding edges")
            print(k-h)
            print("edges")
            print(edges)

    print("Creating graphs")
    plot(avg_degrees, "Average Degree")
    plot(densities, "Density")
    plot(ccs, "Connected Component")
    plot(cs, "Clustering Coefficient")
    plot(edges, "Number of Edges")

if __name__ == "__main__":
	main()