import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

# print(dcc.__version__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True


########################
commValue = 1
getCommActivity = False
homeDf = pd.read_csv('../dataset/vis/stats.csv')
similairtyDf = pd.read_csv('../dataset/combined.csv')
########################

bounds =  dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Lower bound on edges"),
				dbc.Input(id="minEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "5px"}),
            ]
        ),
        html.Div(
            [
                dbc.Label("Upper bound on edges"),
				dbc.Input(id="maxEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "5px"}),

            ]
        ),
        html.Div(
            [
                dbc.Label("Lower bound on nodes"),
				dbc.Input(id="minNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "5px"}),

            ]
        ),
		html.Div(
            [
                dbc.Label("Upper bound on nodes"),
				dbc.Input(id="maxNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "5px"}),


            ]
        ),
    ],
    body=True,
)


index_page = dbc.Container(
    [
        html.H1("Number of nodes and edges in a community"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(bounds, md=3),
                dbc.Col(dcc.Graph(id="main"), md=9),
            ],
            align="center",
        ),
		html.Div(children=[
			dcc.Input(id="getComm", type="number", placeholder="Range: [0, 456]", min=0, max=456, step=1, style={"width": "200px", "margin": "5px"}),
			# dbc.Nav(dbc.NavItem(dbc.NavLink("See community", href="/similarity")), fill=True, pills=True),
			# dbc.NavItem(dbc.NavLink("Active", href="/home", active=True)),
			html.Button(dbc.NavItem(dbc.NavLink("See community", href="/similarity", active=getCommActivity)), id='submit-val', n_clicks=0)
			# html.Button('Submit', id='next', n_clicks=0)
		])
    ],
    id="index_page",
    fluid=True,
)


similarity_layout = dbc.Container(
    [
        html.H1(id='strComm', style={'textAlign':'center'}),
        html.Hr(),
        dbc.Row(
            [
				dbc.Col(dcc.Graph(id="topic")),
				dbc.Col(dcc.Graph(id="temporal")),
            ],
            align="center",
        ),
		html.Div(children=[
			dcc.Input(id="getComm", type="number", placeholder="Range: [0, 456]", min=0, max=456, step=1, style={"width": "200px", "margin": "5px"}),
			# dbc.Nav(dbc.NavItem(dbc.NavLink("See community", href="/similarity")), fill=True, pills=True),
			# dbc.NavItem(dbc.NavLink("Active", href="/home", active=True)),
			html.Button(dbc.NavItem(dbc.NavLink("Change community", href="/similarity", active=getCommActivity)), id='submit-val', n_clicks=0)
			# html.Button('Submit', id='next', n_clicks=0)
		])
    ],
    id="similarity_layout",
    fluid=True,
)

# similarity_layout = dbc.Container(
# 	children=[
# 		html.Div([
# 		html.H1(id='strComm', style={'textAlign':'center'}),
# 		# html.Div(id="strComm")
# 		# dcc.Dropdown(homeDf.community.unique(), value=str(defaultValue), id='dropdown'),
# 	]),
# 	html.Div(className="grap-rows", children=[
# 		# html.Div([
# 		# 	dcc.Graph(id='topic')
# 		# 	# dcc.Graph(id='temporal')
# 		# ], style={'width':'30%', 'align': "left"}),
# 		dbc.Row([
# 			# dcc.Graph(id='topic'),
# 			dbc.Col(dcc.Graph(id="topic")),
# 			dbc.Col(dcc.Graph(id="temporal"))
# 		]),
# 	], ),
# 	],
# 	id="similarity_layout"
# )



app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content',
			 # I added this children attribute
			 children=[index_page, similarity_layout]
			 )
])


# Update the index
@app.callback(
	[dash.dependencies.Output(page, 'style') for page in ['index_page', 'similarity_layout']],
	# I turned the output into a list of pages
	[dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	return_value = [{'display': 'block', 'line-height': '0', 'height': '0', 'overflow': 'hidden'} for _ in range(2)]
	if pathname == '/similarity':
		return_value[1] = {'height': 'auto', 'display': 'inline-block'}
		return return_value
	
	else:
		return_value[0] = {'height': 'auto', 'display': 'inline-block'}
		return return_value




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
	return px.scatter(dff, x="node1", y="node2", color="topic_similarity", width=700, height=600), px.scatter(dff, x="node1", y="node2", color="temporal_similarity", width=700, height=600), "Similarity in Community: {}".format(str(getComm))


# g1, g2 = update_graphs()

if __name__ == '__main__':
	app.run_server(debug=True, port=8050, host='0.0.0.0')