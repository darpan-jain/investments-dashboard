import robin_stocks.robinhood as robin
import pandas as pd
import os
import time
import yaml

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
config = yaml.safe_load(open(f'{DATA_DIR}/creds.yaml'))

# Login to Robinhood
robin.login(username=config['robinhood']['username'],
            password=config['robinhood']['password'],
            expiresIn=86400,
            by_sms=True)
print(f"Logged into Robinhood at {time.strftime('%m/%d/%Y  %H:%M:%S')}")

# Get all positions and user info
my_stocks = robin.build_holdings()
my_crypto = robin.get_crypto_positions()
user = robin.build_user_profile()
print(f"Holdings fetched at {time.strftime('%m/%d/%Y %H:%M:%S')}")

df_stocks = pd.DataFrame(my_stocks)
# Fix the column names and transpose
df_stocks.columns.name = 'symbol'
df_stocks = df_stocks.transpose()
# Preprocess the holdings data
df_stocks['current_value'] = (df_stocks['quantity'] * df_stocks['price']).apply(lambda x: round(x, 3))
df_stocks['buy_price'] = (df_stocks['average_buy_price'] * df_stocks['quantity']).apply(lambda x: round(x, 3))
df_stocks['profit_loss'] = (df_stocks['current_value'] - df_stocks['buy_price']).apply(lambda x: round(x, 3))

df_crypto = pd.DataFrame(my_crypto)
df_user = pd.DataFrame(user, index=[0])

# Export the dataframes to csv
df_stocks.to_csv(f'{DATA_DIR}/stocks.csv')
df_crypto.to_csv(f'{DATA_DIR}/crypto.csv')
df_user.to_csv(f'{DATA_DIR}/user.csv')
print(f"Holdings saved to {DATA_DIR}")
