# Import packages
from dash import Dash, html, dcc, callback, Output, Input, State, callback_context
from dash.exceptions import PreventUpdate

import pandas as pd
import plotly.graph_objects as go

# Incorporate data from local CSV file
df = pd.read_csv('data.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Initialize the app
app = Dash(__name__)

# Global dictionary to store labels
labels_list = []

# App layout
app.layout = html.Div([
    html.H1('My App with Humidity and Temperature Plots'),
    dcc.Graph(id='humidity-temperature-graph'),
    dcc.Input(id='label_start', type='text', placeholder='Start Label'),
    dcc.Input(id='label_end', type='text', placeholder='End Label'),
    html.Button('Confirm', id='confirm-button', n_clicks=0),  # Confirm button
    # In app.layout within app.py
    html.Button('Download Labels', id='download-labels-button', n_clicks=0),
    dcc.Download(id='download-labels')
])

# Add controls to build the interaction
@callback(
    Output('humidity-temperature-graph', 'figure'),
    [Input('confirm-button', 'n_clicks'), Input('humidity-temperature-graph', 'relayoutData')],
    [State('label_start', 'value'), State('label_end', 'value')]
)
def update_graph(n_clicks, relayoutData, label_start, label_end):

    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

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
    if relayoutData:
        fig.update_layout(xaxis_range=[relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']])
        fig.update_layout(yaxis_range=[relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']])
        fig.update_layout(yaxis2_range=[relayoutData['yaxis2.range[0]'], relayoutData['yaxis2.range[1]']])

    return fig


# Add download button to download labels
@callback(
    Output('download-labels', 'data'),
    [Input('download-labels-button', 'n_clicks')],
    prevent_initial_call=True
)
def download_labels(n_clicks):
    if n_clicks is None or n_clicks <= 0:
        raise PreventUpdate
    # Convert labels_list to a DataFrame for easy download
    labels_df = pd.DataFrame(labels_list, columns=['Start Label', 'End Label'])
    # Use dcc.send_data_frame to download the DataFrame as a text file
    return dcc.send_data_frame(labels_df.to_csv, 'labels_list.csv', index=False)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
