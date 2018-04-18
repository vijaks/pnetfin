import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time

def plotGraph(G):
    nx.draw_networkx(G, arrows=True, with_lables=True, node_color='y')
    plt.draw()
    plt.show()


# Start execution time
start_time = time.time()

# Create a graph
G = nx.Graph()
DG = nx.DiGraph()

# Data Filename
filename = 'data.simple'

# Read the CSV into a pandas data frame (df)

df = pd.read_csv(filename, delimiter=',')

print("done reading file to pandas\n")

# Construct the Graph
for index, row in df.iterrows():
    payer = row.ar_id_run
    payee = row.fm_to_ar_id_run
    amt = row.txn_amt
    print(index, ":Adding node", payer, " to ", payee, "amount: ", amt)
    G.add_edge(payer, payee, weight=amt)
    DG.add_edge(payer, payee, weight=amt)

# print "Graph is edges:\n",G.edges()
# print "Directional Graph has edges:\n",DG.edges()

running_time = time.time()
print("System:", (running_time - start_time), "seconds to contruct the network")

print("Graph stat:")
print("Num edges: ", G.number_of_edges())
print("Num nodes: ", G.number_of_nodes())
print("Len: ", len(G))

# create sub graph with connected component
cc = list(nx.connected_components(G))

print("Found: ", len(cc), " subgraph")
i = 0

for sg_set in cc:
    i += 1
    SG = nx.DiGraph(DG.subgraph(sg_set))
    print("Analyse subgraph #", i, SG.edges())
    if not nx.is_directed_acyclic_graph(SG):
        print("Found loop: in sub graph#", i)
        print(SG.edges())
        # plotGraph(SG)
    else:
        print("No loop found!!")
    SG.clear()

