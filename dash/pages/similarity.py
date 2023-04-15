from dash import Dash, html, dcc, callback, Output, Input, register_page
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv('../dataset/combined.csv')
# register_page(__name__, path="/topic")
# app = Dash(__name__)
plot_size = 700

layout = html.Div(children=[
	html.Div([
		html.H1(children='Similarity', style={'textAlign':'center'}),
		dcc.Dropdown(df.community.unique(), id='dropdown'),
	]),
	html.Div(className="grap-rows", children=[
		html.Div([
			dcc.Graph(id='topic')
			# dcc.Graph(id='temporal')
		], style={'width':'30%', 'align': "left"}),
		html.Div([
			# dcc.Graph(id='topic'),
			dcc.Graph(id='temporal')
		], style={'width':'30%', 'align': "right"}),
	]),   
])

	

@callback(
	Output('topic', 'figure'),
	Output('temporal', 'figure'),
	Input('dropdown', 'value'),
	# Input('getComm', 'value')
)

def update_graphs(dropdown, getComm=0):
	value = getComm
	if dropdown:
		value = dropdown
	dff = df[df.community==value]
	return px.scatter(dff, x="node1", y="node2", color="topic_similarity"), px.scatter(dff, x="node1", y="node2", color="temporal_similarity")

# def temporal(value):
#     dff = df[df.community==value]
#     return px.scatter(dff, x="node1", y="node2", color="temporal_similarity")
#     # fig = make_subplots(rows=1, cols=2, column_widths=[plot_size, plot_size], subplot_titles=["Topic Similarity", "Temporal Similarity"])
#     fig.update_layout(height=600, width=1200, coloraxis=dict(colorscale='Viridis'), showlegend=False, hovermode="closest")
#     fig.add_trace(row=1, col=1, trace=go.Scatter(
#         x = dff['node1'].to_list(),
#         y = dff['node2'].to_list(),
#         mode = 'markers',
#         marker=dict(
#             color=dff['topic_similarity'].to_list(),
#             coloraxis='coloraxis',
#             showscale=True
#         ), showlegend=False
#     ))

#     fig.add_trace(row=1, col=2, trace=go.Scatter(
#         x = dff['node1'].to_list(),
#         y = dff['node2'].to_list(),
#         mode = 'markers',
#         marker=dict(
#             color=dff['temporal_similarity'].to_list(),
#             coloraxis='coloraxis',
#             showscale=True
#         ), showlegend=False
#     ))

#     # fig.update_layout()

	
#     return fig

	# return px.scatter(dff, x='node1', y='node2', color='temporal_similarity')

# if __name__ == '__main__':
# 	app.run_server(debug=True)