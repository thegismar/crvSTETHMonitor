from dash import Dash, dash_table, dcc, html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('data.csv', index_col=False)

fig = go.Figure(data=[go.Scatter(x=df.date, y=df.net_value)])

app = Dash(__name__)
app.title = "Curve staked ETH/stETH pool monitor"
app.layout = html.Div(children=[

    html.H1(children='Curve staked ETH/stETH pool monitor'),

    html.Div(children='''
        x-axis: time, y-axis net worth including lido interest.
    '''),

    dcc.Graph(figure=fig),

    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="80")
