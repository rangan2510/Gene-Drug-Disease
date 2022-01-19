import sqlite3
import networkx as nx
import dgl
import torch as th
import scipy.sparse as sp
import pandas as pd
#loading data from Disgenet database

try:
    conn=sqlite3.connect('disgenet_2020.db')
except Exception as e:
    print("cannot open database",str(e))

#gene.csv creation
sql="""
select * from geneAttributes

"""
df=pd.read_sql_query(sql,conn)
df1=df.drop(columns=['Unnamed: 0','Unnamed: 0.1','geneId','geneDescription','pLI','DSI','DPI'])
df1.to_csv('genes.csv')

#disease.csv creation
sql="""
select * from diseaseAttributes

"""
df=pd.read_sql_query(sql,conn)
df1=df.drop(columns=['Unnamed: 0','diseaseId','type'])
df1.to_csv('diseases_1.csv')

#edges.csv creation
sql="""
select * from geneDiseaseNetwork

"""
df=pd.read_sql_query(sql,conn)
df1=df.drop(columns=['Unnamed: 0','NID','source','association','associationType','sentence','pmid','score','EL','EI','year'])
df.to_csv(r'fullgraph.txt', header=None, index=None, sep=' ', mode='a')
conn.close()

#networkx graph creation

G=nx.read_edgelist('./fullgraph.txt')
print(nx.info(G))

#dgl graph creation
DG=dgl.from_networkx(G)
print(DG)

# saving the dgl graph as a bin file
from dgl.data.utils import save_graphs
graph_labels = {"glabel": th.tensor([0])}
save_graphs("./dgl_graph.bin", [g1], graph_labels)

#loading the bin file as a dgl graph
from dgl.data.utils import load_graphs
glist, label_dict = load_graphs("./dgl_graph.bin", [0])
