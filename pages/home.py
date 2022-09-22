import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import sqlite3

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Data Dashboard'),

])


