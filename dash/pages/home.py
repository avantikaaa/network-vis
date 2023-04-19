from dash import Dash, html, dcc, callback, Output, Input, register_page
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc


from pages import similarity

getCommActivity = False
df = pd.read_csv('../dataset/vis/stats.csv')
register_page(__name__, path='/')
# app = Dash(__name__)
plot_size = 700
layout = html.Div(children=[
	html.Div([
		html.H1(children='Similarity', style={'textAlign':'center'}),
	]),
	html.Div(children = [
	
		dbc.Col([
			html.Div(children = [
				dcc.Input(id="minEdges", type="number", placeholder="lower bound for edge_count", min=1, max=2230, step=1, style={"width": "200px", "margin": "5px"}),
				dcc.Input(id="maxEdges", type="number", placeholder="upper bound for edge_count", min=1, max=2230, step=1, style={"width": "200px", "margin": "5px"}),
				dcc.Input(id="minNodes", type="number", placeholder="lower bound for node_count", min=2, max=398, step=1, style={"width": "200px", "margin": "5px"}),
				dcc.Input(id="maxNodes", type="number", placeholder="upper bound for node_count", min=2, max=398, step=1, style={"width": "200px", "margin": "5px"}),
			], style={"align": "center"}),

			html.Div([
				dcc.Graph(id='main'),
			])
		]),
		html.Div(children=[
			dcc.Input(id="getComm", type="number", placeholder="community id", min=0, max=456, step=1, style={"width": "200px", "margin": "5px"}),
			# dbc.Nav(dbc.NavItem(dbc.NavLink("See community", href="/similarity")), fill=True, pills=True),
			# dbc.NavItem(dbc.NavLink("Active", href="/home", active=True)),
			html.Button(dbc.NavItem(dbc.NavLink("See community", href="/similarity", active=getCommActivity)), id='submit-val', n_clicks=0)
			# html.Button('Submit', id='next', n_clicks=0)
		])
	
		
	]),

	
])

	

@callback(
	Output('main', 'figure'),
	Input('minNodes', 'value'),
	Input('maxNodes', 'value'),
	Input('minEdges', 'value'),
	Input('maxEdges', 'value'),
	Input('getComm', 'value'),

)

def update_graph(low_node, high_node, low_edge, high_edge, getComm):
	if not low_node:
		low_node = 2
	if not high_node:
		high_node = 398
	if not low_edge:
		low_edge = 1
	if not high_edge:
		high_edge = 2230
	similarity.setDefaultVal(getComm)
	getCommActivity = True
	# print("getComm:", getComm)
	
	# print(low_edge, high_edge, low_node, high_node)
	if low_node > high_node or low_edge > high_edge:
		return px.scatter(df, x='edge_count', y='node_count', color='community')
	
	dff = df.loc[(df['node_count'] >= low_node) & (df['node_count'] <= high_node) & (df['edge_count'] >= low_edge) & (df['edge_count'] <= high_edge)]
	return px.scatter(dff, x='edge_count', y='node_count', color='community')

# @callback(
# 	Output("", ""),
# 	Input('getComm', 'value')
# )

def setVal(getComm):
	# similarity.setDefaultVal(getComm)
	similarity.defaultValue = getComm





# if __name__ == '__main__':
# 	app.run_server(debug=True)
