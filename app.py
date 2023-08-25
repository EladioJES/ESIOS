

import requests
import datetime
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='API Data Dashboard'),
    html.Div(children='''
        Select start and end timestamps:
    '''),
    dcc.Input(id='start-timestamp', type='text', value='2023-04-01T00:00:00'),
    dcc.Input(id='end-timestamp', type='text', value='2023-04-19T00:00:00'),
    html.Div(children='''
        Enter API token:
    '''),
    dcc.Input(id='api-token', type='text', value=''),
    html.Button('Submit', id='submit-button'),
    html.Div(id='scatter-plots')  # Placeholder for scatter plots
])

@app.callback(
    dash.dependencies.Output('scatter-plots', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('start-timestamp', 'value'),
     dash.dependencies.State('end-timestamp', 'value'),
     dash.dependencies.State('api-token', 'value')])
def update_plot(n_clicks, start_timestamp, end_timestamp, api_token):
    # Your API request and DataFrame preparation code here...
    
        # Parse the start and end timestamps using the datetime module
    start_dt = datetime.datetime.fromisoformat(start_timestamp)
    end_dt = datetime.datetime.fromisoformat(end_timestamp)
    
    # Make the API request using the requests library
    headers = dict()
    headers['Accept'] = 'application/json; application/vnd.esios-api-v1+json'
    headers['Content-Type'] = 'application/json'
    headers['Host'] = 'api.esios.ree.es'
    headers['x-api-key'] = api_token
    headers['Cookie'] = ''
    
    # print(api_token)
    
    params = {'start_date': start_dt.isoformat(), 'end_date': end_dt.isoformat()}
    
    # https://api.esios.ree.es/indicators/1373?start_date=' + '2023-04-10T00:00:00' + 'Z&end_date=' + '2023-04-10T23:00:00' + 'Z'
    response = requests.get('https://api.esios.ree.es/indicators/600', headers=headers, params=params)
    print(response.status_code)
    print(response.url)
    print(response.json()['indicator']['values'])
    if response.status_code != 200:
        raise ValueError(f'Request failed with status code {response.status_code}: {response.text}')
    data = response.json()['indicator']['values']
    
    # Convert the API response to a Pandas DataFrame
    df = pd.DataFrame(data)
    df.datetime = pd.to_datetime(df.datetime, utc = True)
    # df.datetime = df.datetime.tz_convert('Europe/Madrid')

    # Create a list to hold the dcc.Graph components
    graphs = []

    for category in df['geo_name'].unique():
        filtered_df = df.loc[df['geo_name'] == category]
        trace = go.Scatter(
            x=pd.to_datetime(filtered_df['datetime'], utc=True),
            y=filtered_df['value'],
            mode='lines',
            name=category
        )
        
        layout = go.Layout(
             title=category,  # Adding the title here
            xaxis={'title': 'Timestamp'},
            yaxis={'title': 'Value'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )

        graphs.append(
            html.Div(
                dcc.Graph(
                    id=f'scatter-plot-{category}',
                    figure={
                        'data': [trace],
                        'layout': layout
                    }
                ),
                style={'display': 'inline-block'}
            )
        )

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)  # Run the app
