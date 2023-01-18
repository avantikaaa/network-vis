import pandas as pd
import networkx as nx
from community import community_louvain


def dictToCSV(d, name1, name2, filename):
    node = []
    comm = []
    for key in d:
        node.append(key)
        comm.append(d[key])
    
    df = pd.DataFrame({name1: node, name2: comm})
    df.to_csv(filename, index=False)
    return df

df = pd.read_csv("../IEEE VIS papers 1990-2021 - Main dataset.csv")
df = df[['AuthorNames']]
df = df.dropna()

authors = df['AuthorNames'].to_list()

G = nx.Graph()

for current in authors:
	# print(current)
	lst = current.split(";")
	for i in range(len(lst)):
		for j in range(i+1, len(lst)):
			G.add_edge(lst[i], lst[j])


partition = community_louvain.best_partition(G)


# print(partition)
# node = []
# comm = []
# for key in partition:
#     node.append(key)
#     comm.append(partition[key])

# df = pd.DataFrame({"author": node, "community": comm})
# df.to_csv("community.csv", index=False)

df = dictToCSV(partition, "author", "community", "community.csv")
test = df['community'].value_counts().to_dict()

dictToCSV(test, "community", "population", "community_stats.csv")