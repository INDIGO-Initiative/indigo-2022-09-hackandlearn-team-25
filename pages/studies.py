import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import sqlite3

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Studies'),
    html.Div([
        "Year: ",
        dcc.Input(id='study-year-min-input', value='2010', type='number'),
        " to ",
        dcc.Input(id='study-year-max-input', value='2023', type='number'),
        " (inclusive)",
    ]),
    dcc.Graph(
        id='study-design-graph',
    )
])



@callback(
    Output(component_id='study-design-graph', component_property='figure'),
    Input(component_id='study-year-min-input', component_property='value'),
    Input(component_id='study-year-max-input', component_property='value'),
)
def update_study_design_graph(study_year_min, study_year_max):
    connection = sqlite3.connect('data/research-projects-database.sqlite')
    df = pd.read_sql_query(
        "SELECT study_design, count(*) AS c FROM study WHERE study_design IS NOT NULL AND date_publication_year >= ? AND date_publication_year <= ? GROUP BY study_design",
        connection,
        params = [
            study_year_min,
            study_year_max
        ]
    )
    fig = px.bar(df, x="study_design", y="c")
    connection.close()
    return fig
