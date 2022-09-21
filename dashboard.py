import dash
from dash import Dash, html, dcc, Input, Output


app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Data Dashboard'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)

