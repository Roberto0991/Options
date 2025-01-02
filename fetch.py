import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_options_data(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    expirations = stock.options
    
    # Filter expirations for the next 3 months
    three_months_later = (datetime.now() + pd.DateOffset(months=3)).date()
    valid_expirations = [date for date in expirations if datetime.strptime(date, '%Y-%m-%d').date() <= three_months_later]

    all_options = []
    
    for date in valid_expirations:
        opt = stock.option_chain(date)
        
        # Process call options
        calls = opt.calls
        calls['type'] = 'Call'
        calls['distance'] = abs(calls['strike'] - current_price)
        
        # Process put options
        puts = opt.puts
        puts['type'] = 'Put'
        puts['distance'] = abs(puts['strike'] - current_price)
        
        # Combine and sort by distance, take the top 3 closest to market price
        options = pd.concat([calls, puts])
        closest_options = options.sort_values(by='distance').head(3)[['type', 'strike', 'lastPrice', 'lastTradeDate', 'expiration']]
        
        # Append data
        all_options.append(closest_options)
    
    # Concatenate all options data
    return pd.concat(all_options, ignore_index=True)

def save_to_csv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Tickers to process
tickers = ['INTC', 'CLF', 'MSTR']

# Prepare the DataFrame
all_data = pd.DataFrame()

# Fetch and aggregate data
for ticker in tickers:
    print(f"Fetching options for {ticker}")
    options_data = fetch_options_data(ticker)
    options_data['ticker'] = ticker
    all_data = pd.concat([all_data, options_data], ignore_index=True)

# Save the data to a CSV file
today_date = datetime.now().strftime('%Y-%m-%d')
filename = f"options_data_{today_date}.csv"
save_to_csv(all_data, filename)
