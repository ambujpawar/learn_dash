# Import packages
from dash import Dash, html, dcc, callback, Output, Input, State, callback_context
from dash.exceptions import PreventUpdate

import pandas as pd
import plotly.graph_objects as go


# Initialize the app
app = Dash(__name__)

# Global dictionary to store labels
labels_list = []

# App layout
app.layout = html.Div([
    html.H1('My App with Humidity and Temperature Plots'),
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'Amsterdam', 'value': 'amsterdam'},
            {'label': 'Eindhoven', 'value': 'eindhoven'},
            {'label': 'Rotterdam', 'value': 'rotterdam'}
        ],
        placeholder="Select a city",
    ),
    dcc.Tabs([
        dcc.Tab(label='Humidity and Temperature Graph', children=[
            dcc.Graph(id='humidity-temperature-graph'),
            dcc.Input(id='label_start', type='text', placeholder='Start Label'),
            dcc.Input(id='label_end', type='text', placeholder='End Label'),
            html.Button('Confirm', id='confirm-button', n_clicks=0),  # Confirm button
            # In app.layout within app.py
            html.Button('Download Labels', id='download-labels-button', n_clicks=0),
            dcc.Download(id='download-labels')
        ]),
        dcc.Tab(label='Labels', children=[
            dcc.Graph(id='labels-graph')
        ])
    ])
])

# Add controls to build the interaction
@callback(
    Output('humidity-temperature-graph', 'figure'),
    [   
        Input('city-dropdown', 'value'),
        Input('confirm-button', 'n_clicks'),
        Input('humidity-temperature-graph', 'relayoutData'),
    ],
    [State('label_start', 'value'), State('label_end', 'value')]
)
def update_graph(city, n_clicks, relayoutData, label_start, label_end):
    global df
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Load the city data if the dropdown value changes
    if trigger_id == 'city-dropdown' and city:
        global labels_list
        labels_list = []  # Clear the labels list if a new city is selected
        print("Labels list cleared due to city change.")
        df = pd.read_csv(f'{city}.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # only update the labels list if the button is clicked
    if trigger_id == 'confirm-button' and n_clicks > 0:
        labels_list.append((label_start, label_end))
        print(f"Labels dictionary updated: {labels_list}")

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['humidity'], name="Humidity", mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['temperature'], name="Temperature", mode='lines+markers', yaxis="y2"))

    # Add titles and labels
    fig.update_layout(
        title="Humidity and Temperature Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Humidity",
        legend_title="Variable",
        yaxis=dict(title='Humidity', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
        yaxis2=dict(title='Temperature', titlefont=dict(color='red'), tickfont=dict(color='red'), overlaying='y', side='right'),
        template='plotly_dark',
        autosize=True,
    )

    # Apply zoom levels from relayoutData if available
    if 'xaxis.range[0]' in relayoutData:
        fig.update_layout(xaxis_range=[relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']])
        fig.update_layout(yaxis_range=[relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']])
        fig.update_layout(yaxis2_range=[relayoutData['yaxis2.range[0]'], relayoutData['yaxis2.range[1]']])

    return fig


# Add download button to download labels
@callback(
    Output('download-labels', 'data'),
    [Input('download-labels-button', 'n_clicks')],
    [State('city-dropdown', 'value')],
    prevent_initial_call=True
)
def download_labels(n_clicks, city):
    if n_clicks is None or n_clicks <= 0:
        raise PreventUpdate
    # Convert labels_list to a DataFrame for easy download
    labels_df = pd.DataFrame(labels_list, columns=['Start Label', 'End Label'])
    # Use dcc.send_data_frame to download the DataFrame as a text file
    filename = f'labels_{city}.csv' if city else 'labels_list.csv'
    return dcc.send_data_frame(labels_df.to_csv, filename, index=False)


# Callback for updating the labels graph
@callback(
    Output('labels-graph', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_labels_graph(city):
    print(f"City: {city}")
    if city:
        df = pd.read_csv(f'{city}.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['label'], name="Labels", mode='lines+markers'))
        fig.update_layout(
            title="Labels Over Time",
            xaxis_title="Timestamp",
            yaxis_title="Labels",
            template='plotly_dark',
            autosize=True,
        )
        return fig
    else:
        raise PreventUpdate


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
