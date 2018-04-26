import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time
import operator

filename = 'simple'

# class FinTxNet()

class txEdge():
    def __init__(self,payer,payee,amt):
        self.payer = payer
        self.payee = payee
        self.amt = amt
        self.myList = []
        return
    def canAdd(self,payer,payee):
        result = False
        if ((self.payer==payer) and (self.payee==payee)):
            print("Can add")
            result = True
        return result
    def add(self,amt):
        if ((self.payer == payer) and (self.payee == payee)):
            print("error adding edge")
        self.amt = self.amt + amt
        self.myList.append(amt)
        return
    def myCount(self):
        return len(self.myList)
    def myList(self):
        return self.myList

class netTxGraph():
    def __init__(self):
        self.mg = nx.MultiDiGraph()
        self.dg = nx.DiGraph()
        self.loopList = []
        return
    def show(self):
        print("------------------------------")
        print("Show graphs:")
        print("MultiDiGraph:")
        for line in nx.generate_edgelist(self.mg):
            print(line)
        print("------------------------------")
        print("DiGraph:")
        for line in nx.generate_edgelist(self.dg):
            print(line)
        print("------------------------------")
#        plotGraph(self.mg)
        return
    def stat(self):
        print("------------------------------")
        print("Graph stat:")
        print("Num edges: ", self.mg.number_of_edges())
        print("Num nodes: ", self.mg.number_of_nodes())
        print("Len: ", len(self.mg))
        print("------------------------------")
        return
    def add_edge(self,fn,tn,amt):
        self.mg.add_edge(payer,payee,weight=amt)
        if self.dg.has_edge(payer,payee):
            curWeight = self.dg.get_edge_data(payer,payee)
            addedWeight = float(curWeight['weight']) + amt
            self.dg.add_edge(payer,payee,weight=addedWeight)
            print("Adding edges:",payer," to ",payee," w ",addedWeight)
        else:
            self.dg.add_edge(payer,payee,weight=amt)
        return
    def sumWeight(self,edge):
        myWeight = 0;
        return myWeight
    def __str__(self):
        return f'Graph with {len(self.mg)} nodes'
    def plot(self):
        plotGraph(self.mg)
        return
    def totAMT(self):
        return totAMT(self.mg)
    def avgAMT(self):
        return (self.totAMT()/self.mg.number_of_edges())
    def highDegreeNode(self):
        degList = self.mg.degree()
        degList = sortedList(degList)
        printList(degList,10,'All')
        degList = self.mg.out_degree()
        degList = sortedList(degList)
        printList(degList,10,'Out')
        degList = self.mg.in_degree()
        degList = sortedList(degList)
        printList(degList,10,'In')
        return
    def findLoop(self):
        # create sub graph with connected component
        cc = list(nx.connected_components(self.dg.to_undirected()))

        print("Found: ", len(cc), " subgraph")
        i = 0
        loopList = list()
        numLoop = 0

        for sg_set in cc:
            i += 1
            SG = nx.DiGraph(self.dg.subgraph(sg_set))
            print("Analyse subgraph #", i, SG.edges())
            if not nx.is_directed_acyclic_graph(SG):
                numLoop += 1
                loopList.append(SG)
                print("Found loop: in sub graph#", i)
                print(SG.edges())
                mytotAMT = totAMT(SG)
                print("Total amount is: ", mytotAMT)
                print("Avg amount is: ", mytotAMT/SG.number_of_edges())
            # plotGraph(SG)
            else:
                print("No loop found!!")
            SG.clear()
        return numLoop

def printList(myList,numItem,degType):
    print("Top",numItem,"Node with Highest",degType,"degree:")
    i = 0
    for node in myList[0:numItem]:
        i+=1
        print(i,": ",node)
    return

def sortedList(myList):
    myList = sorted(myList, key=operator.itemgetter(1), reverse=True)
    return myList

def plotGraph(G):
    nx.draw_networkx(G, arrows=True, with_lables=True, node_color='y')
    plt.draw()
    plt.show()

def totAMT(G):
    tot = 0
    for (u, v, d) in G.edges(data=True):
        tot = tot + d['weight']
    return tot

# Start execution time
start_time = time.time()

# Create a graph
TG = netTxGraph()

# Read the CSV into a pandas data frame (df)
# filename = 'data.simple' # has loop

try:
    df = pd.read_csv(filename, delimiter=',')
except Exception as e:
    print("Error in reading", filename)
    print(e)

print("done reading file to pandas\n")

# Construct the Graph
for index, row in df.iterrows():
    payer = str(row.ar_id_run)
    payee = str(row.fm_to_ar_id_run)
    amt = row.txn_amt
    print(index, ":Adding node", payer, " to ", payee, "amount: ", amt)
    TG.add_edge(payer, payee,amt)

running_time = time.time()
print("Time: Construct graph: ",running_time-start_time)

TG.show()
TG.stat()
TG.highDegreeNode()
numLoop = TG.findLoop()

if (numLoop > 0):
    print("-----------------------------")
    print("Found ", numLoop, " loop in this network")
else:
    print("-----------------------------")
    print("Found no loop in this network")