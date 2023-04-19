import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

print(dcc.__version__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True


########################
commValue = 1
getCommActivity = False
homeDf = pd.read_csv('../dataset/vis/stats.csv')
similairtyDf = pd.read_csv('../dataset/combined.csv')
########################


index_page = html.Div(
	# I added this id attribute
	id='index_page',
	children=[
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
			],
	# I added this style attribute
	style={'display': 'block', 'line-height':'0', 'height': '0', 'overflow': 'hidden'}
)

page_1_layout = html.Div(
	# I added this id attribute
	id='page_1_layout',
	children=[
		html.H1('Page 1'),
		dcc.Dropdown(
			id='page-1-dropdown',
			options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
			value='LA'
		),
		html.Div(id='page-1-content'),
		html.Br(),
		dcc.Link('Go to Page 2', href='/page-2'),
		html.Br(),
		dcc.Link('Go back to home', href='/'),
	],
	# I added this style attribute
	style={'display': 'block', 'line-height': '0', 'height': '0', 'overflow': 'hidden'}

)


similarity_layout = html.Div(
	id="similarity_layout",
	children=[
		html.Div([
		html.H1(children='Similarity', style={'textAlign':'center'}),
		html.Div(id="strComm")
		# dcc.Dropdown(homeDf.community.unique(), value=str(defaultValue), id='dropdown'),
	]),
	html.Div(className="grap-rows", children=[
		# html.Div([
		# 	dcc.Graph(id='topic')
		# 	# dcc.Graph(id='temporal')
		# ], style={'width':'30%', 'align': "left"}),
		html.Div([
			# dcc.Graph(id='topic'),
			dcc.Graph(id="topic"),
			dcc.Graph(id="temporal")
		]),
	]),
	]
)


page_2_layout = html.Div(
	# I added this id attribute
	id='page_2_layout',
	children=[
		html.H1('Page 2'),
		html.Div(id='page-2-content'),
		html.Br(),
		dcc.Link('Go to Page 1', href='/page-1'),
		html.Br(),
		dcc.Link('Go back to home', href='/'),
	],
	# I added this style attribute
	style={'display': 'block', 'line-height': '0', 'height': '0', 'overflow': 'hidden'}
)

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content',
			 # I added this children attribute
			 children=[index_page, page_1_layout, page_2_layout, similarity_layout]
			 )
])


# Update the index
@app.callback(
	[dash.dependencies.Output(page, 'style') for page in ['index_page', 'page_1_layout', 'page_2_layout', 'similarity_layout']],
	# I turned the output into a list of pages
	[dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	return_value = [{'display': 'block', 'line-height': '0', 'height': '0', 'overflow': 'hidden'} for _ in range(4)]

	if pathname == '/page-1':
		return_value[1] = {'height': 'auto', 'display': 'inline-block'}
		return return_value
	elif pathname == '/page-2':
		return_value[2] = {'height': 'auto', 'display': 'inline-block'}
		return return_value

	elif pathname == '/similarity':
		return_value[3] = {'height': 'auto', 'display': 'inline-block'}
		return return_value
	
	else:
		return_value[0] = {'height': 'auto', 'display': 'inline-block'}
		return return_value


@app.callback(dash.dependencies.Output('page-1-content', 'children'),
			  [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
	return 'You have selected "{}"'.format(value)


@app.callback(Output('page-2-content', 'children'),
			  [Input('page-1-dropdown', 'value')])
def page_2(value):
	return 'You selected "{}"'.format(value)


@app.callback(
	Output('main', 'figure'),
	Input('minNodes', 'value'),
	Input('maxNodes', 'value'),
	Input('minEdges', 'value'),
	Input('maxEdges', 'value')

)
def home_graph(low_node, high_node, low_edge, high_edge):
	if not low_node:
		low_node = 2
	if not high_node:
		high_node = 398
	if not low_edge:
		low_edge = 1
	if not high_edge:
		high_edge = 2230
	
	# if getComm:
	# 	commValue = getComm
	# 	getCommActivity = True
	# similarity.setDefaultVal(getComm)
	# getCommActivity = True
	# print("getComm:", getComm)
	
	# print(low_edge, high_edge, low_node, high_node)
	if low_node > high_node or low_edge > high_edge:
		return px.scatter(homeDf, x='edge_count', y='node_count', color='community')
	
	dff = homeDf.loc[(homeDf['node_count'] >= low_node) & (homeDf['node_count'] <= high_node) & (homeDf['edge_count'] >= low_edge) & (homeDf['edge_count'] <= high_edge)]
	return px.scatter(dff, x='edge_count', y='node_count', color='community')

@app.callback(
	Output("topic", 'figure'),
	Output("temporal", 'figure'),
	Output("strComm", "children"),
	Input('getComm', 'value')
)

def similarity_graphs(getComm):
	value = str(getComm)
	# print("whhhhhha", getComm)
	# if dropdown:
	# 	value = dropdown
	dff = similairtyDf[similairtyDf.community==value]
	# print(dff.head())
	return px.scatter(dff, x="node1", y="node2", color="topic_similarity"), px.scatter(dff, x="node1", y="node2", color="temporal_similarity"), "Community {}".format(str(getComm))


# g1, g2 = update_graphs()

if __name__ == '__main__':
	app.run_server(debug=True, port=8050, host='0.0.0.0')