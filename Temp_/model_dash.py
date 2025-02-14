import dash
from dash import dcc, html
import plotly.graph_objs as go
import pymongo
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import time

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["smart_cooling"]
sensor_collection = db["sensor_data"]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Real-Time Data Center Monitoring Dashboard"), className="text-center")
        ]),
        dbc.Row([
            dbc.Col(html.Div("Select Data and Plot Type:"), width=12),
            dbc.Col(
                dcc.Dropdown(
                    id="data-dropdown",
                    options=[
                        {"label": "Time", "value": "time"},
                        {"label": "Data Cube", "value": "data_cube"},
                        {"label": "Zone", "value": "zone"},
                        {"label": "Manual-Agent", "value": "manual-agent"}
                    ],
                    value="time",  # Default value
                    multi=False
                ),
                width=6
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="plot-type-dropdown",
                    options=[
                        {"label": "Line Plot (Temp vs Fan Speed)", "value": "line"},
                        {"label": "Scatter Plot", "value": "scatter"},
                        {"label": "Box Plot", "value": "box"}
                    ],
                    value="line",  # Default value
                    multi=False
                ),
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="live-graph"), width=12)
        ])
    ])
])

# Function to fetch and prepare data
def fetch_sensor_data():
    sensor_data = list(sensor_collection.find().sort("timestamp", -1).limit(100))  # Fetch last 100 records
    flat_data = []
    for record in sensor_data:
        timestamp = record["timestamp"]
        for i in range(len(record["temperature"])):
            flat_data.append({
                "timestamp": timestamp,
                "temperature": record["temperature"][i],
                "humidity": record["humidity"][i],
                "fan_speed": record["fan_speed"][i],
                "data_cube": i + 1
            })
    df = pd.DataFrame(flat_data)
    return df

# Update graph every 5 seconds
@app.callback(
    Output("live-graph", "figure"),
    [Input("data-dropdown", "value"), Input("plot-type-dropdown", "value")]
)
def update_graph(data_type, plot_type):
    df = fetch_sensor_data()

    if data_type == "time":
        x_axis = df["timestamp"]
    elif data_type == "data_cube":
        x_axis = df["data_cube"]
    elif data_type == "zone":
        # Assuming zones are defined (e.g., DataCube 1 and 2 are Zone 1)
        df['zone'] = df["data_cube"].apply(lambda x: 1 if x in [1, 2] else 2)
        x_axis = df['zone']
    else:
        x_axis = df["humidity"]  # For manual-agent, example using humidity

    # Generate the required plot based on plot type selection
    if plot_type == "line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_axis, y=df["temperature"], mode='lines+markers', name="Temperature"))
        fig.add_trace(go.Scatter(x=x_axis, y=df["fan_speed"], mode='lines+markers', name="Fan Speed"))
        fig.update_layout(title="Temperature vs Fan Speed", xaxis_title="X-Axis", yaxis_title="Values")

    elif plot_type == "scatter":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["temperature"], y=df["fan_speed"], mode='markers', name="Temp vs Fan Speed"))
        fig.update_layout(title="Scatter Plot - Temp vs Fan Speed", xaxis_title="Temperature", yaxis_title="Fan Speed")

    elif plot_type == "box":
        fig = go.Figure()
        fig.add_trace(go.Box(y=df["temperature"], name="Temperature"))
        fig.add_trace(go.Box(y=df["fan_speed"], name="Fan Speed"))
        fig.update_layout(title="Box Plot", yaxis_title="Values")
    
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
