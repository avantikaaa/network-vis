import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True


########################
commValue = 1
getCommActivity = False
homeDf = pd.read_csv('./stats.csv')
similairtyDf = pd.read_csv('./combined.csv')
print(homeDf['community'].to_list())
########################
# ,
		# dbc.Row(
		# 	[
		# 		dbc.Col(dcc.Graph(id="topic_full"), md=6),
		# 		dbc.Col(dcc.Graph(id="temporal_full"), md=6)
		# 	]
		# )

bounds = dbc.Container([
	dbc.Card(
		[
			html.Div(
				[
					dbc.Label("Lower bound on edges"),
					dbc.Input(id="minEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "3px"}),
				]
			),
			html.Div(
				[
					dbc.Label("Upper bound on edges"),
					dbc.Input(id="maxEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "3px"}),

				]
			),
			html.Div(
				[
					dbc.Label("Lower bound on nodes"),
					dbc.Input(id="minNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "3px"}),

				]
			),
			html.Div(
				[
					dbc.Label("Upper bound on nodes"),
					dbc.Input(id="maxNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "3px"}),


				]
			),
		],
		body=True,
	),
	dcc.Input(id="getComm", type="number", placeholder="Range: [0, 456]", min=0, max=456, step=1, style={"width": "200px", "margin": "5px"}),
	html.Button(dbc.NavItem(dbc.NavLink("See community", href="/similarity", active=getCommActivity)), id='submit-val', n_clicks=0)
	
])
# bounds =  dbc.Card(
#     [
#         html.Div(
#             [
#                 dbc.Label("Lower bound on edges"),
# 				dbc.Input(id="minEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "3px"}),
#             ]
#         ),
#         html.Div(
#             [
#                 dbc.Label("Upper bound on edges"),
# 				dbc.Input(id="maxEdges", type="number", placeholder="Range = [1, 2230]", min=1, max=2230, step=1, style={"margin": "3px"}),

#             ]
#         ),
#         html.Div(
#             [
#                 dbc.Label("Lower bound on nodes"),
# 				dbc.Input(id="minNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "3px"}),

#             ]
#         ),
# 		html.Div(
#             [
#                 dbc.Label("Upper bound on nodes"),
# 				dbc.Input(id="maxNodes", type="number", placeholder="Range = [2, 398]", min=2, max=398, step=1, style={"margin": "3px"}),


#             ]
#         ),
#     ],
#     body=True,
# )


index_page = dbc.Container(
    [
        html.H1("Number of nodes and edges in a community", style={'marginTop': 20, 'textAlign': 'center'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(bounds, md=3),
                dbc.Col(dcc.Graph(id="main"), md=9),
            ],
            align="center",
        ),
		# html.Div(children=[
		# 	dcc.Input(id="getComm", type="number", placeholder="Range: [0, 456]", min=0, max=456, step=1, style={"width": "200px", "margin": "5px"}),
		# 	html.Button(dbc.NavItem(dbc.NavLink("See community", href="/similarity", active=getCommActivity)), id='submit-val', n_clicks=0)
		# ]),
		dbc.Row(
		[
			dbc.Col(dcc.Graph(id="topic_full"), md=6),
			dbc.Col(dcc.Graph(id="temporal_full"), md=6)
		]
	)
    ],
    id="index_page",
    fluid=True,
)

seriation = dbc.Row([
	dbc.Col(html.H5("Seriate Matrix:"), md=2),
	dbc.Col(dcc.RadioItems(
		options=[
			{'value': 'node', 'label': 'Default'},
			{'value': 'communityOrdering', 'label': 'Community'},
			{'value': 'edgeOrdering', 'label': 'Number of Edges'},
			{'value': 'topicOrdering', 'label': 'Topic Similarity'},
			{'value': 'temporalOrdering', 'label': 'Temporal Similarity'},
		],
		value='node',
		inline=True,
		labelStyle={'marginRight':'20px'},
		id="matrixSeriation"
	), ),
])


similarity_layout = dbc.Container(
    [
		dbc.Col(html.H1(id='strComm', style={'marginTop': 20}), style={'textAlign': 'center'}),
        html.Hr(),
	    dbc.Row(
			[
				dbc.Col(html.H5("Order by:"), width="auto"),
				dbc.Col(dcc.RadioItems(
					options=[
						{'value': 'node', 'label': 'Default'},
						{'value': 'communityOrdering', 'label': 'Community'},
						{'value': 'edgeOrdering', 'label': 'Number of Edges'},
						{'value': 'topicOrdering', 'label': 'Topic Similarity'},
						{'value': 'temporalOrdering', 'label': 'Temporal Similarity'},
					],
					value='node',
					inline=True,
					labelStyle={'marginRight':'20px', 'marginTop':'2px'},
					id="matrixSeriation"
				), ),
				dbc.Col(html.Button(dbc.NavItem(dbc.NavLink("Back", href="/")), id='go-home', n_clicks=0, style={"width": "100px", "align": "left", 'marginTop': 5}), align="right", width="auto"),
			],
	
		),
		
        dbc.Row(
            [
				dbc.Col([
					dcc.Graph(id="topic"),
					# html.H5("Topic Similarity Graph", style={'textAlign': "center", "marginTop": 0}),
				]),
				dbc.Col([
					dcc.Graph(id="temporal"),
					# html.H5("Temporal Similarity Graph", style={'textAlign': "center", "marginTop": 0}),
				]),
            ],
            align="center",
        ),
    ],
    id="similarity_layout",
    fluid=True,
)


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
	return_value = [{'display': 'block', 'lineHeight': '0', 'height': '0', 'overflow': 'hidden'} for _ in range(2)]
	if pathname == '/similarity':
		return_value[1] = {'height': 'auto', 'display': 'inline-block'}
		return return_value
	
	else:
		return_value[0] = {'height': 'auto', 'display': 'inline-block'}
		return return_value




@app.callback(
	Output('main', 'figure'),
	Output('topic_full', 'figure'),
	Output('temporal_full', 'figure'),
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
	
	if low_node > high_node or low_edge > high_edge:
		return px.scatter(homeDf, x='edge_count', y='node_count', color='community'), px.scatter(similairtyDf, x="node1", y="node2", height=750, color="topic_similarity", color_continuous_scale='Plasma', title="Topic Similarity", labels={"node1": "node", "node2": "node", "topic_similarity": 'Topic Similarity'}), px.scatter(similairtyDf, x="node1", y="node2", height=750, color="temporal_similarity", color_continuous_scale='Viridis', title="Temporal Similarity", labels={"node1": "node", "node2": "node", "temporal_similarity": 'Temporal Similarity'})
	
	else:
		dff = homeDf.loc[(homeDf['node_count'] >= low_node) & (homeDf['node_count'] <= high_node) & (homeDf['edge_count'] >= low_edge) & (homeDf['edge_count'] <= high_edge)]

		sim_filtered = similairtyDf[similairtyDf['community'].isin(dff['community'].to_list())]

		return px.scatter(dff, x='edge_count', y='node_count', color='community'), px.scatter(sim_filtered, x="node1", y="node2", color="topic_similarity", color_continuous_scale='Plasma', title="Topic Similarity", height=750, labels={"node1": "node", "node2": "node", "topic_similarity": 'Topic Similarity'}), px.scatter(sim_filtered, x="node1", y="node2", height=750, color="temporal_similarity", color_continuous_scale='Viridis', title="Temporal Similarity", labels={"node1": "node", "node2": "node", "temporal_similarity": 'Temporal Similarity'})




def seriate(df, field, getComm):
	x_tmp = df['node1'].to_list()
	y_tmp = df['node2'].to_list()

	ordering = pd.read_csv("seriation.csv")
	mapping = ordering[field].to_list()
	x = []
	y = []
	for i in x_tmp:
		x.append(mapping[i])
	for i in y_tmp:
		y.append(mapping[i])

	new_df = pd.DataFrame(data={
		"node1": x,
		"node2": y,
		"topic_similarity": df['topic_similarity'].to_list(),
		"temporal_similarity": df['temporal_similarity'].to_list()
	})

	try:
		plot1 = px.scatter(new_df, x='node1', y='node2', color='topic_similarity', height=800, width=800, color_continuous_scale='Plasma', title="Topic Similarity", labels={"node1": "node", "node2": "node", "topic_similarity": 'Topic Similarity'})
	except:
		plot1 = px.scatter(new_df, x='node1', y='node2', color='topic_similarity', height=800, width=800, color_continuous_scale='Plasma', title="Topic Similarity", labels={"node1": "node", "node2": "node", "topic_similarity": 'Topic Similarity'})
	
	try:
		plot2 = px.scatter(new_df, x='node1', y='node2', color='temporal_similarity', height=800, width=800, color_continuous_scale='Viridis', title="Temporal Similarity", labels={"node1": "node", "node2": "node", "temporal_similarity": 'Temporal Similarity'})
	except:
		plot2 = px.scatter(new_df, x='node1', y='node2', color='temporal_similarity', height=800, width=800, color_continuous_scale='Viridis', title="Temporal Similarity", labels={"node1": "node", "node2": "node", "temporal_similarity": 'Temporal Similarity'})


	
	
	return (plot1, plot2, "Similarity in Community: {}".format(str(getComm)))

@app.callback(
	Output("topic", 'figure'),
	Output("temporal", 'figure'),
	Output("strComm", "children"),
	Input('getComm', 'value'),
	Input('matrixSeriation', 'value')
)



def similarity_graphs(getComm, matrixSeriation):
	value = str(getComm)
	if value == 'None':
		value = '11'
	dff = similairtyDf[similairtyDf.community==value]

	return seriate(dff, matrixSeriation, value)



if __name__ == '__main__':
	app.run_server(debug=True, port=8050, host='0.0.0.0')