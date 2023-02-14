import pandas as pd

df_auth = pd.read_csv("../layer1/community.csv")


def dictToCSV(d, name1, name2, filename):
	node = []
	comm = []
	for key in d:
		node.append(key)
		comm.append(d[key])
	
	df = pd.DataFrame({name1: node, name2: comm})
	df.to_csv(filename, index=False)
	return df
	
authors = {}
i = 0
mat = []
for auth in df_auth["author"].to_list():
	authors[auth] = i
	mat.append([0]*(26))
	mat[i][0] = i
	i += 1

dictToCSV(authors, "author", "num", "authorToInt.cvs")

df = pd.read_csv("../IEEE VIS papers 1990-2021 - Main dataset.csv")

df = df[["AuthorNames", "Year"]]

for ind in df.index:
	auth = df["AuthorNames"][ind]
	for a in auth.split(";"):
		mat[authors[a]][df["Year"][ind]-1990] += 1
