#%%
import pandas as pd
import networkx as nx

df = pd.read_csv("edges.csv")
# %%
edge_keys = df.columns.to_list()[2:]
feats = ["feat_" + str(x) for x in range(len(edge_keys))]
#%%
df.columns = ["node1","node2"] + feats
#%%
G = nx.from_pandas_edgelist(df,"node1","node2", edge_attr=feats, create_using=nx.MultiDiGraph())
nx.write_gml(G,"temp.gml")
# %%
import dgl
g = dgl.from_networkx(G, edge_attrs=feats)

#%%
import dgl.function as fn
for i,f in enumerate(feats):
    ndata_scheme = "nfeat_" + str(i)
    g.update_all(fn.copy_e(f,'m'),fn.sum('m',ndata_scheme))


#%%
from dgl.data.utils import save_graphs
save_graphs("./data.bin", g)

# %%
