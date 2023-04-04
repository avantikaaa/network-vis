from dash import Dash, html
import pandas as pd

# app = Dash(__name__)

df_weight = pd.read_csv("../dataset/layer3/pearson_distance.csv.zip", compression="zip")
import plotly.express as px
# df = px.data.iris()
# print(df.describe())
# fig = px.scatter(df, x="sepal_width", y="sepal_length", color='petal_length')
# fig.show()

print("here")
import glob
edge_files = glob.glob("../dataset/community/*.edge")
# print(edge_files)

new_mapping = {}
count = 0

tmp = []

for file in edge_files:
    f = open(file, "r")
    for line in f.readlines():
        a, b = map(int, line[:-1].split())
        if a not in new_mapping:
            new_mapping[a] = count
            count += 1
        if b not in new_mapping:
            new_mapping[b] = count
            count += 1
        tmp.append([new_mapping[a], new_mapping[b], df_weight.loc[a].at(b)])
        tmp.append([new_mapping[b], new_mapping[a], df_weight.loc[a].at(b)])
    f.close()
    print(file)

df = pd.DataFrame(tmp, columns=["node1", "node2", "weight"])
df.to_csv("../dataset/new_mapping.csv", index=False)
print("fig")
fig = px.scatter(df, x="node1", y="node2", color='weight')
fig.show()



# app.layout = html.Div([
#     html.Div(children='Hello World')
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)