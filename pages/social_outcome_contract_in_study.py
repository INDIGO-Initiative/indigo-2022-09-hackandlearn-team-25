import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas
import sqlite3
from contextlib import closing

dash.register_page(__name__)


layout = html.Div(children=[
    html.H1(children='Social Outcome contracts in Study'),
    html.H2(children='Changes/Variations'),
    dcc.Graph(
        id='report1'
    ),
    html.H2(children='Costs and resources'),
    dcc.Graph(
        id='report2'
    ),
    html.H2(children='Ecosystem/System strengthening effects'),
    dcc.Graph(
        id='report3'
    ),
    html.H2(children='Scalability and Sustainability of SOC'),
    dcc.Graph(
        id='report4'
    ),
    dcc.Interval(
        id="load_interval",
        n_intervals=0,
        max_intervals=0, #<-- only run once
        interval=1
    ),
])



@callback(
    Output(component_id='report1', component_property='figure'),
    Input(component_id="load_interval", component_property="n_intervals"),
)
def report1(load_interval):
    data = _get_report_data([
        ('reports_changes_in_service_delivery_intervention_specific','service delivery - intervention specific'),
        ('reports_changes_in_person_level_outcomes','person-level outcomes'),
        ('reports_unintended_effects','unintended effects'),
        ('reports_auxiliary_resource_or_parallel_reforms_occurring_alongside_soc','Auxiliary resource or parallel reforms'),
        ('reports_on_acceptability_of_SOC_political_cultural','acceptability of SOC (political/cultural)'),
        ('reports_implications_for_management_information_systems','implications for management information systems'),
    ])
    #print("1" + str(data))
    df = pandas.DataFrame(data)
    # See https://community.plotly.com/t/inconsistent-callback-error-updating-scatter-plot/46754/8 for the hack for this terrible try / except
    try:
        fig = px.bar(df, x="label", y=["present",'absent', 'missing'], color_discrete_sequence=['blue','red','yellow'])
    except Exception:
        fig = px.bar(df, x="label", y=["present", 'absent', 'missing'], color_discrete_sequence=['blue', 'red','yellow'])
    return fig

@callback(
    Output(component_id='report2', component_property='figure'),
    Input(component_id="load_interval", component_property="n_intervals"),
)
def report2(load_interval):
    data = _get_report_data([
        ('reports_costs_and_resource_implications','Reports on costs and resource implications - especially transaction costs'),
    ])
    #print("2" + str(data))
    df = pandas.DataFrame(data)
    try:
        fig = px.bar(df, x="label", y=["present",'absent', 'missing'], color_discrete_sequence=['blue','red','yellow'])
    except Exception:
        fig = px.bar(df, x="label", y=["present", 'absent', 'missing'], color_discrete_sequence=['blue', 'red','yellow'])
    return fig


@callback(
    Output(component_id='report3', component_property='figure'),
    Input(component_id="load_interval", component_property="n_intervals"),
)
def report3(load_interval):
    data = _get_report_data([
        ('reports_ecosystem_or_system_strengthening_effects','Reports on ecosystem or system strengthening effects - i.e. implications beyond the SOC parties'),
    ])
    #print("3" + str(data))
    df = pandas.DataFrame(data)
    try:
        fig = px.bar(df, x="label", y=["present",'absent', 'missing'], color_discrete_sequence=['blue','red','yellow'])
    except Exception:
        fig = px.bar(df, x="label", y=["present", 'absent', 'missing'], color_discrete_sequence=['blue', 'red','yellow'])
    return fig


@callback(
    Output(component_id='report4', component_property='figure'),
    Input(component_id="load_interval", component_property="n_intervals"),
)
def report4(load_interval):
    data = _get_report_data([
        ('reports_scalability','Reports on scale/scalability of the SOC approach'),
        ('reports_long_term_sustainment_and_legacy_effects','Reports on long-term sustainment and \'post-SOC\' legacy effects'),
    ])
    #print("4" + str(data))
    df = pandas.DataFrame(data)
    try:
        fig = px.bar(df, x="label", y=["present",'absent', 'missing'], color_discrete_sequence=['blue','red','yellow'])
    except Exception:
        fig = px.bar(df, x="label", y=["present", 'absent', 'missing'], color_discrete_sequence=['blue', 'red','yellow'])
    return fig



def _get_report_data(field_and_label_list):
    connection = sqlite3.connect('data/research-projects-database.sqlite')
    data = {
        'label': [],
        'present': [],
        'absent': [],
        'missing': [],
    }
    with closing(connection.cursor()) as cursor:
        for field, label in field_and_label_list:

            data['label'].append(label)

            cursor.execute(
                "SELECT count(*) AS c FROM social_outcomes_contract WHERE "+field+" = 'present' OR "+field+" = 'Present'",
                []
            )
            data['present'].append(cursor.fetchone()[0])

            cursor.execute(
                "SELECT count(*) AS c FROM social_outcomes_contract WHERE  "+field+" = 'absent' OR "+field+" = 'Absent'",
                []
            )
            data['absent'].append(cursor.fetchone()[0])

            cursor.execute(
                "SELECT count(*) AS c FROM social_outcomes_contract WHERE NOT ( "+field+" = 'present' OR "+field+" = 'Present' OR "+field+" = 'absent' OR "+field+" = 'Absent')",
                []
            )
            data['missing'].append(cursor.fetchone()[0])

    connection.close()
    return data
