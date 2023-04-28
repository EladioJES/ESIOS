import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Load data
# df = pd.read_csv('data.csv')

# Define app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Spot prices in Europe"),
    html.H5("Pick X-axis data"),
    # html.Label('X-axis'),
    dcc.Dropdown(
        id='x-axis',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]
    ),
    html.H5("Pick Y-axis data"),
    # html.Label('Y-axis'),
    dcc.Dropdown(
        id='y-axis',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[2]
    ),
    html.Label('Categories'),
    dcc.Dropdown(
        id='categories',
        options=[{'label': cat, 'value': cat} for cat in df['geo_name'].unique()],
        value=df['geo_name'].unique(),
        multi=True
    ),
    dcc.Graph(id='scatter-plot')
])

# Define callback
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value'),
     dash.dependencies.Input('categories', 'value')])
def update_plot(x_col, y_col, categories):
    traces = []
    for cat in categories:
        filtered_df = df[df['geo_name'] == cat]  # Filter the DataFrame by category
        trace = go.Scatter(
            x=filtered_df[x_col],
            y=filtered_df[y_col],
            mode='lines',
            line=dict(shape='hv', width=2),  # Set the line shape to horizontal-vertical step
            name=cat  # Set the name of the trace to the category name
        )
        traces.append(trace)
    layout = go.Layout(
        xaxis={'title': x_col},
        yaxis={'title': y_col},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        hovermode='closest'
    )
    return {'data': traces, 'layout': layout}

# Run app
if __name__ == '__main__':
    app.run()
