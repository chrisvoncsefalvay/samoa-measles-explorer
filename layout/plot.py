import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

TICK_VALUES = ["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", "50y-above",
               "missing"]

MARKER_RED = "rgb(224, 46, 28)"
MARKER_BLUE = "rgb(43, 71, 100)"

TITLE_LAYOUT = dict(
    family="Helvetica Neue",
    size=23,
    color=MARKER_BLUE
)

PLOT_RESOLUTION = dict(width=1600,
                       height=768)


def plot_mortality_morbidity(data: pd.DataFrame) -> dcc.Graph:
    dt = data.groupby(["date", "status"]).sum().reset_index()
    dates = list(dt["date"].unique())
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    cfr = data[data["status"] == "deaths"].groupby("date").sum() / data[data["status"] == "cases"].groupby("date").sum()

    # Case trace
    fig.add_trace(go.Bar(name="Cases",
                         x=dates,
                         y=dt[dt["status"] == "cases"]["value"],
                         text=100 * cfr,
                         hovertemplate="%{x}<br>"
                                       "<b>%{y} cases<br>"
                                       "CFR: %{text:.2f}</b>",
                         texttemplate="           CFR: %{text:.2f}%",
                         textposition="inside"),
                  secondary_y=False)

    fig.update_traces(marker_color=MARKER_BLUE)

    # Mortality line
    fig.add_trace(go.Scatter(name="Deaths",
                             x=dates,
                             y=dt[dt["status"] == "deaths"]["value"],
                             hovertemplate="%{x}<br>"
                                           "<b>%{y} deaths</b>"),
                  secondary_y=True)

    fig.update_xaxes(tickangle=45,
                     tickformat="%a %d-%m-%Y",
                     automargin=True)

    fig.update_layout(title_text=f"<b>Mortality and morbidity from measles</b><br>"
                                 f"<span style='font-size: 12;'>{data.date.max()} | samoa-measl.es</span>",
                      height=600)

    fig.update_yaxes(range=[0, 1.05 * data[data["status"] == "cases"].groupby("date").sum()["value"].max()],
                     secondary_y=False)
    fig.update_yaxes(range=[0, 1.05 * data[data["status"] == "deaths"].groupby("date").sum()["value"].max()],
                     secondary_y=True)

    fig["layout"]["titlefont"].update(**TITLE_LAYOUT)

    return dcc.Graph(figure=fig,
                     config={"toImageButtonOptions": PLOT_RESOLUTION,
                             "displaylogo": False})


def plot_by_age_group(data: pd.DataFrame) -> dcc.Graph:
    fig = go.Figure()
    max_date = data["date"].max()
    dt = data[data["date"] == max_date].reset_index()

    fig.add_trace(go.Bar(x=dt[dt["status"] == "cases"]["age_group"],
                         y=dt[dt["status"] == "cases"]["value"],
                         name="Cases",
                         marker_color=MARKER_BLUE))
    fig.add_trace(go.Bar(x=dt[dt["status"] == "deaths"]["age_group"],
                         y=dt[dt["status"] == "deaths"]["value"],
                         name="Deaths",
                         marker_color=MARKER_RED))

    fig.update_xaxes(
        ticktext=["<5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", ">50y", "missing"],
        tickvals=TICK_VALUES,
        tickangle=45,
        automargin=True
    )

    fig.update_layout(yaxis_type="log",
                      title_text=f"<b>Age distribution of cases</b><br>"
                                 f"<span style='font-size: 12;'>{data.date.max()} | samoa-measl.es</span>",
                      xaxis=dict(categoryorder="array",
                                 categoryarray=["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y",
                                                "40-49y", "50y-above", "missing"]),
                      height=600)

    fig["layout"]["titlefont"].update(**TITLE_LAYOUT)

    return dcc.Graph(figure=fig,
                     config={"toImageButtonOptions": PLOT_RESOLUTION,
                             "displaylogo": False})


def plot_cfr(data: pd.DataFrame) -> dcc.Graph:
    fig = go.Figure()

    df = data.pivot_table(index=["date", "age_group"], columns="status", values="value").reset_index()
    df["CFR"] = df["deaths"] / df["cases"]

    fig.add_trace(go.Box(x=df["age_group"],
                         y=df["CFR"],
                         marker_color=MARKER_BLUE))

    mean_cfr = df["deaths"].sum() / df["cases"].sum()

    fig.add_shape(go.layout.Shape(
        type="line",
        y0=mean_cfr,
        y1=mean_cfr,
        x0=TICK_VALUES[0],
        x1=TICK_VALUES[-1],
        line=dict(
            color=MARKER_RED,
            width=2,
            dash="dot",
        )
    ))

    fig.add_annotation(go.layout.Annotation(
        x=TICK_VALUES[-2],
        y=mean_cfr + 0.002,
        text=f"Mean CFR: {100 * mean_cfr:.2f}%",
        showarrow=False,
        ax=30,
        ay=0
    ))

    fig.update_xaxes(
        ticktext=["<5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", ">50y", "missing"],
        tickvals=TICK_VALUES,
        tickangle=45,
        automargin=True
    )

    fig.update_yaxes(tickformat=".2%",
                     tick0=0.0,
                     dtick=0.005)

    fig.update_layout(xaxis=dict(categoryorder="array",
                                 categoryarray=["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y",
                                                "40-49y", "50y-above", "missing"]),
                      title_text=f"<b>Case-fatality statistics by age</b><br>"
                                 f"<span style='font-size: 12;'>{data.date.max()} | samoa-measl.es</span>",
                      height=600)

    fig["layout"]["titlefont"].update(**TITLE_LAYOUT)

    return dcc.Graph(figure=fig,
                     config={"toImageButtonOptions": PLOT_RESOLUTION,
                             "displaylogo": False})
