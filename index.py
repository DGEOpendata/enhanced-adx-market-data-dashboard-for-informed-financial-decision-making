python
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load dataset
data_url = 'https://opendata.abudhabi.ae/finance/adx-market-bulletin-30-04-2026.xlsx'
data = pd.read_excel(data_url)

# Basic data cleaning
columns_to_keep = ['Company Name', 'Market Capitalization', 'Trading Volume', 'Sector', 'Last Close Price']
data = data[columns_to_keep]

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Enhanced ADX Market Data Dashboard"),
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': i, 'value': i} for i in data['Sector'].unique()],
        placeholder='Select a Sector'
    ),
    dcc.Graph(id='sector-performance-chart'),
    dcc.Graph(id='market-capitalization-chart')
])

@app.callback(
    [Output('sector-performance-chart', 'figure'),
     Output('market-capitalization-chart', 'figure')],
    [Input('sector-dropdown', 'value')]
)
def update_charts(selected_sector):
    filtered_data = data if selected_sector is None else data[data['Sector'] == selected_sector]
    sector_chart = px.bar(filtered_data, x='Company Name', y='Trading Volume', color='Last Close Price', title='Sector Performance')
    market_cap_chart = px.pie(filtered_data, values='Market Capitalization', names='Company Name', title='Market Capitalization Distribution')
    return sector_chart, market_cap_chart

if __name__ == '__main__':
    app.run_server(debug=True)
