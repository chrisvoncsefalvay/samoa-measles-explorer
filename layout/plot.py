import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

TICK_VALUES = ["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", "50y-above",
               "missing"]

MARKER_RED = "rgb(224, 46, 28)"
MARKER_BLUE = "rgb(43, 71, 100)"

def plot_mortality_morbidity(data: pd.DataFrame) -> dcc.Graph:
    dt = data.groupby(["date", "status"]).sum().reset_index()
    dates = list(dt["date"].unique())
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Case trace
    fig.add_trace(go.Bar(name="Cases",
                         x=dates,
                         y=dt[dt["status"] == "cases"]["value"]),
                  secondary_y=False)

    fig.update_traces(marker_color=MARKER_BLUE)

    # Mortality line
    fig.add_trace(go.Scatter(name="Deaths", x=dates, y=dt[dt["status"] == "deaths"]["value"]),
                  secondary_y=True)


    return dcc.Graph(figure=fig)


def plot_by_age_group(data: pd.DataFrame) -> dcc.Graph:
    fig = go.Figure()
    dt = data.groupby(["age_group", "status"]).sum().reset_index()

    fig.add_trace(go.Bar(x=dt[dt["status"] == "deaths"]["age_group"],
                         y=dt[dt["status"] == "deaths"]["value"],
                         name="Deaths",
                         marker_color=MARKER_RED))
    fig.add_trace(go.Bar(x=dt[dt["status"] == "cases"]["age_group"],
                         y=dt[dt["status"] == "cases"]["value"],
                         name="Cases",
                         marker_color=MARKER_BLUE))

    fig.update_layout(barmode="relative")
    fig.update_layout(yaxis_type="log")

    fig.update_xaxes(
        ticktext=["<5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", ">50y", "missing"],
        tickvals=TICK_VALUES
    )

    fig.update_layout(xaxis=dict(categoryorder="array",
                                 categoryarray=["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y",
                                                "40-49y", "50y-above", "missing"]))

    return dcc.Graph(figure=fig)


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
        text=f"Mean CFR: {100*mean_cfr:.2f}%",
        showarrow=False,
        ax=30,
        ay=0
    ))

    fig.update_xaxes(
        ticktext=["<5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y", "40-49y", ">50y", "missing"],
        tickvals=TICK_VALUES
    )

    fig.update_yaxes(tickformat=".2%")

    fig.update_layout(xaxis_tickformat='%d %B (%a)<br>%Y', )

    fig.update_layout(xaxis=dict(categoryorder="array",
                                 categoryarray=["0-5m", "6-11m", "1-4y", "5-9y", "10-14y", "15-19y", "20-29y", "30-39y",
                                                "40-49y", "50y-above", "missing"]))

    return dcc.Graph(figure=fig)
