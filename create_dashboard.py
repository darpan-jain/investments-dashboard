import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Read the dataframes from csv
df_stocks = pd.read_csv('data/stocks.csv', header=0)

# Add column for total dollar value of each stock
df_stocks['current_value'] = (df_stocks['quantity'] * df_stocks['price']).apply(lambda x: round(x, 3))
# Add column for buy price of the stock
df_stocks['buy_price'] = (df_stocks['average_buy_price'] * df_stocks['quantity']).apply(lambda x: round(x, 3))

# Add column for total profit or loss of each stock
df_stocks['profit_loss'] = (df_stocks['current_value'] - df_stocks['buy_price']).apply(lambda x: round(x, 3))

# df_crypto = pd.read_csv('data/crypto.csv')
# df_user = pd.read_csv('data/user.csv')
print(f"Dataframes loaded from {DATA_DIR}. Creating investment dashboard...")

# Print all columns in the stocks dataframe
print(df_stocks.columns)

# Create a visual dashboard for stock holdings with 4 subplots
fig = make_subplots(rows=2,
                    cols=2,
                    specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "pie"}, {"type": "bar"}]],
                    subplot_titles=("Profit/Loss", "Current Value", "Buy Price", "Quantity"),
                    # vertical_spacing=0.1,
                    # horizontal_spacing=0.1,
                    # shared_xaxes=True,
                    # shared_yaxes=True,
                    )

fig.update_layout(height=800, width=1000, title_text="Investment Dashboard", showlegend=False)

# Create a bar chart for stock holdings
fig_stocks_bar = px.bar(df_stocks, x='symbol', y='profit_loss', title='Profit/Loss')
fig_stocks_bar.update_traces(marker_color=['green' if x > 0 else 'red' for x in df_stocks.profit_loss])

# Create a pie chart for stock holdings current value of each stock
fig_stocks_pie = px.pie(df_stocks, values='current_value', names=df_stocks.name, title='Current Value')
fig_stocks_pie.update_traces(textposition='inside', textinfo='percent+label')

# Create a bar chart for stock holdings buy price of each stock
fig_stocks_buy = px.bar(df_stocks, x='symbol', y='buy_price', title='Buy Price')

# TBD add more viz

# Add only the bar chart for stock holdings to the first subplot
fig.add_trace(fig_stocks_bar['data'][0], row=1, col=1)
fig.add_trace(fig_stocks_buy['data'][0], row=1, col=2)
fig.add_trace(fig_stocks_pie['data'][0], row=2, col=1)

# Show the pie chart
fig.show()
