import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# 🔹 Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SmartCoolingSystem"
COLLECTION_NAME = "Processed_AI_Responses"

# Create Dash app
app = dash.Dash(__name__)
app.title = "📊 Smart Cooling System Dashboard"

# Function to fetch data from MongoDB
def fetch_data():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ID
    client.close()

    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame(columns=["timestamp", "data_cube", "temperature", "humidity", "fan_speed", "heat", "current"])

    df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime
    return df.sort_values(by="timestamp", ascending=True)

# Initial Data Fetch
df = fetch_data()

# Debug: Print the total number of records
print(f"Total records fetched: {len(df)}")

# Unique DataCube IDs
unique_datacubes = df["data_cube"].unique() if not df.empty else []

# Dash Layout
app.layout = html.Div([
    html.H1("📊 Smart Cooling System Analytics Dashboard", style={"textAlign": "center"}),

    # 🔹 Dropdown to Select DataCube
    html.Label("Select DataCube:"),
    dcc.Dropdown(
        id="datacube-dropdown",
        options=[{"label": f"DataCube {i}", "value": i} for i in unique_datacubes],
        value=unique_datacubes[0] if len(unique_datacubes) > 0 else None,
        clearable=False
    ),

    # 🔹 Date Picker Range (Set default to full range)
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id="date-picker",
        start_date=df["timestamp"].min().date() if not df.empty else None,
        end_date=df["timestamp"].max().date() if not df.empty else None,
        display_format="YYYY-MM-DD"
    ),

    # 🔹 Graphs
    dcc.Graph(id="temp-humidity-line-chart"),
    dcc.Graph(id="fan-speed-bar-chart"),
    dcc.Graph(id="heat-scatter-plot"),
    dcc.Graph(id="current-trend-line-chart"),

    # 🔹 Auto-Refresh Interval (10 sec)
    dcc.Interval(id="interval-component", interval=10*1000, n_intervals=0)
])

# Callback to update graphs
@app.callback(
    [
        Output("temp-humidity-line-chart", "figure"),
        Output("fan-speed-bar-chart", "figure"),
        Output("heat-scatter-plot", "figure"),
        Output("current-trend-line-chart", "figure")
    ],
    [
        Input("datacube-dropdown", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("interval-component", "n_intervals")
    ]
)
def update_charts(selected_cube, start_date, end_date, _):
    df = fetch_data()  # Refresh data

    if df.empty:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Debug: Print number of records before filtering
    # print(f"Records before filtering: {len(df)}")

    # 🔹 Filter by DataCube and Date Range
    df = df[(df["data_cube"] == selected_cube) & (df["timestamp"].between(start_date, end_date))]

    # Debug: Print number of records after filtering
    # print(f"Records after filtering: {len(df)}")

    if df.empty:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # 🔹 Temperature & Humidity Line Chart (Ensure x-axis is properly formatted)
    fig1 = px.line(
        df, x="timestamp", y=["temperature", "humidity"],
        title="🌡️ Temperature & Humidity Trends", markers=True
    )
    fig1.update_xaxes(tickformat="%Y-%m-%d %H:%M:%S", tickangle=45)  # Ensure all timestamps are visible

    # 🔹 Fan Speed Bar Chart
    fig2 = px.bar(df, x="timestamp", y="fan_speed", title="💨 Fan Speed Over Time", color="fan_speed")
    fig2.update_xaxes(tickformat="%Y-%m-%d %H:%M:%S", tickangle=45)

    # 🔹 Heat Scatter Plot
    fig3 = px.scatter(
        df, x="temperature", y="heat", size="heat", color="data_cube",
        title="🔥 Temperature vs Heat Scatter Plot"
    )

    # 🔹 Current Trend Line Chart
    fig4 = px.line(
        df, x="timestamp", y="current",
        title="⚡ Current Consumption Trends", markers=True
    )
    fig4.update_xaxes(tickformat="%Y-%m-%d %H:%M:%S", tickangle=45)

    return fig1, fig2, fig3, fig4

# Run App
if __name__ == "__main__":
    app.run_server(debug=True)
