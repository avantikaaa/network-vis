from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Page 1", href="/")),
                dbc.NavItem(dbc.NavLink("Page 2", href="/similarity")),
            ] ,
            brand="Multipage Dash App",
            brand_href="/",
            # color="dark",
            # dark=True,
        ), 
    ])

    return layout