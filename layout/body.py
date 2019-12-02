import dash_bootstrap_components as dbc
import dash_html_components as html
from layout.sidecart_texts import get_sidecart


# Column contents

sidecart_contents: list = get_sidecart(context="mortality")

# Plot object

plot_object: html.Div = html.Div([], id="plot-object")

# Column components

graph_area: dbc.Col = dbc.Col(children=[plot_object],
                              className="col-xl-9 col-lg-9 col-md-9 col-sm-12 col-12",
                              id="graph-area-contents")

sidecart: dbc.Col = dbc.Col(sidecart_contents,
                            className="col-xl-3 col-lg-3 col-md-3 col-sm-12 col-12",
                            id="sidecart-contents")

# Body structure

graph_row: dbc.Row = dbc.Row([graph_area, sidecart], className="mt-4")

body = dbc.Container([graph_row])
