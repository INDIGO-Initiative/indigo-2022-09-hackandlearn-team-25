import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas
import sqlite3
from contextlib import closing

dash.register_page(__name__)


layout = html.Div(children=[
    html.H1(children='Social Outcome contracts in Study'),

    dcc.Graph(
        id='reports4'
    ),
    dcc.Interval(
        id="load_interval",
        n_intervals=0,
        max_intervals=0, #<-- only run once
        interval=1
    ),
])



@callback(
    Output(component_id='reports4', component_property='figure'),
    Input(component_id="load_interval", component_property="n_intervals"),
)
def report4(load_interval):
    connection = sqlite3.connect('data/research-projects-database.sqlite')
    with closing(connection.cursor()) as cursor:

        cursor.execute(
            "SELECT count(*) AS c FROM social_outcomes_contract WHERE reports_scalability = 'present' OR reports_scalability = 'Present'",
            []
        )
        reports_scalability_present = cursor.fetchone()[0]

        cursor.execute(
            "SELECT count(*) AS c FROM social_outcomes_contract WHERE reports_long_term_sustainment_and_legacy_effects = 'present' OR reports_long_term_sustainment_and_legacy_effects = 'Present'",
            []
        )
        reports_long_term_sustainment_and_legacy_effects_present = cursor.fetchone()[0]

        cursor.execute(
            "SELECT count(*) AS c FROM social_outcomes_contract WHERE NOT( reports_scalability = 'present' OR reports_scalability = 'Present')",
            []
        )
        reports_scalability_absent = cursor.fetchone()[0]

        cursor.execute(
            "SELECT count(*) AS c FROM social_outcomes_contract WHERE NOT (reports_long_term_sustainment_and_legacy_effects = 'present' OR reports_long_term_sustainment_and_legacy_effects = 'Present')",
            []
        )
        reports_long_term_sustainment_and_legacy_effects_absent = cursor.fetchone()[0]

    data = {
        'label': [
            'reports_scalability',
            'reports_long_term_sustainment_and_legacy_effects'
        ],
        'present': [
            reports_scalability_present,
            reports_long_term_sustainment_and_legacy_effects_present
        ],
        'absent': [
            reports_scalability_absent,
            reports_long_term_sustainment_and_legacy_effects_absent
        ]
    }
    #print(data)
    df = pandas.DataFrame(data)
    #print(df)
    fig = px.bar(df, x="label", y=["present",'absent'], color_discrete_sequence=['blue','red'])
    connection.close()
    return fig



