from dash import Dash, dash_table, dcc, html
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = Dash(__name__)
app.title = "Curve staked ETH/stETH pool monitor"


def serve_layout():
    # Load the data.
    df = pd.read_csv('data.csv', index_col=False)
    df.sort_values(by='timestamp', ascending=False, inplace=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df.date, y=df.net_value, name="net value"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.date, y=df.eth_tokens, name="eth tokens"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=df.date, y=df.steth_tokens, name="steth tokens"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=df.date, y=df.pool_tokens, name="curve tokens"),
        secondary_y=True,
    )

    # Render the layout.

    return html.Div(children=[

        html.H1(children='Curve staked ETH/stETH pool monitor'),

        html.Div(children='''
        x-axis: time, y-axis 1 net worth including lido interest, y-axis 2 total amount of eth that can be withdrawn
    '''),

        dcc.Graph(figure=fig),

        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ])


app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="80")
