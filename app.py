from typing import Tuple, List, Any
import flask
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache
from layout import body, navbar
from layout.plot import plot_mortality_morbidity, plot_by_age_group, plot_cfr
from layout.sidecart_texts import get_sidecart

# App
server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.FLATLY],
                server=server,
                meta_tags=[
                    {"name": "description",
                     "content": "Exploring the human impact of the measles outbreak in Samoa."},
                    {"name": "viewport",
                     "content": "width=device-width, initial-scale=1.0"},
                    {"name": "og:title",
                     "content": "Moe: the Measles Outbreak Explorer"},
                    {"name": "og:type",
                     "content": "website"},
                    {"name": "og:url",
                     "content": "http://samoa-measl.es/"},
                    {"name": "og:description",
                     "content": "Exploring the human impact of the measles outbreak in Samoa."},
                    {"name": "og:locale",
                     "content": "en_US"},
                    {"name": "og:site_name",
                     "content": "Moe – The Measles Outbreak Explorer"},
                    {"name": "og:image",
                     "content": "http://samoa-measl.es/assets/og_img.jpg"},
                    {"name": "og:image:type",
                     "content": "image/jpeg"},
                    {"name": "og:image:width",
                     "content": "400"},
                    {"name": "og:image:height",
                     "content": "300"}])

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.title = "Measles Outbreak Explorer (Moe)"

# Cache

cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': "filesystem",
    'CACHE_DIR': "cache",
})


# Loader
@cache.memoize(timeout=1800)
def get_data() -> pd.DataFrame:
    data_url = "https://raw.githubusercontent.com/chrisvoncsefalvay/samoa-measles-2019/master/data/cumulative_data.csv"
    data = pd.read_csv(data_url,
                       sep=";",
                       parse_dates=[1],
                       cache_dates=True)
    return data


location = dcc.Location(id="url", refresh=True)

app.layout = html.Div([location, navbar, body])


@cache.memoize(600)
@app.callback([dash.dependencies.Output("sidecart-contents", "children"),
               dash.dependencies.Output("plot-object", "children"),
               dash.dependencies.Output("last-update", "children")],
              [dash.dependencies.Input("url", "pathname")])
def display_page(pathname: str) -> Tuple[list, List[dcc.Graph], str]:
    data = get_data()
    last_update = str(data["date"].unique().max()) + " UTC"
    if pathname == "/" or pathname == "/mortality-morbidity":
        return get_sidecart(context="mortality"), [plot_mortality_morbidity(data)], last_update
    elif pathname == "/by-age-group":
        return get_sidecart(context="age_group"), [plot_by_age_group(data)], last_update
    elif pathname == "/cfr":
        return get_sidecart(context="cfr"), [plot_cfr(data)], last_update
    elif pathname == "/about":
        return get_sidecart(context="mortality"), [plot_mortality_morbidity(data)], last_update
    else:
        return get_sidecart(context="mortality"), [plot_mortality_morbidity(data)], last_update


if __name__ == '__main__':
    app.run_server(debug=True)
