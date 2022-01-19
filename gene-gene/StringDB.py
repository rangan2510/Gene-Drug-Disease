#%% get intersect
from socket import inet_aton
import pandas as pd
disease_genes = pd.read_csv("../disease-gene/genes.csv")
disease_genes = disease_genes["geneName"]
disease_genes.rename({'geneName':'gene_symbol'}, inplace = True)
drug_genes = pd.read_csv("../drug-gene/gene.csv")
drug_genes = drug_genes["gene_symbol"]
# %%
di_ge_set = set(disease_genes.to_list())
dr_ge_set = set(drug_genes.to_list())
common_ge_set = di_ge_set.intersection(dr_ge_set)
# %%
f = open("common_genes.csv", 'w')
for item in list(common_ge_set):
    f.write(item + "\n")
f.close()
# %% 
# UPLOAD COMMON GENES TO STRINGDB, GET GETWORK
# READ NETWORK TO REFINE GENE SET
string_genes = pd.read_csv("string_interactions_short.tsv", sep="\t")
# %%
common_ge_set = set(string_genes["#node1"].to_list()).intersection(set(string_genes["node2"].to_list()))
# %%
# rewrite
f = open("common_genes.csv", 'w')
for item in list(common_ge_set):
    f.write(item + "\n")
f.close()
# %%
string_genes = string_genes[["#node1", "node2","neighborhood_on_chromosome",
"gene_fusion", "phylogenetic_cooccurrence", "homology", "coexpression",
"experimentally_determined_interaction", "database_annotated", "automated_textmining", "combined_score"
]]
# %%
string_genes = string_genes.rename({"#node1": "node1"}, axis=1)
string_genes.to_csv("edges.csv", index=False)
# %%
