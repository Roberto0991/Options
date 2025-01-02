import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_options_data(ticker, target_months):
    stock = yf.Ticker(ticker)
    options_data = []

    # Target expiration months
    target_expirations = [date for date in stock.options if datetime.strptime(date, '%Y-%m-%d').strftime('%b %Y') in target_months]

    for exp_date in target_expirations:
        # Fetch options data for each target expiration date
        opt_chain = stock.option_chain(exp_date)
        for option_type, options in [('Calls', opt_chain.calls), ('Puts', opt_chain.puts)]:
            options['Type'] = option_type  # Add a new column for option type
            options['Expiration'] = exp_date  # Add a new column for expiration date
            options_data.append(options[['Type', 'Expiration', 'strike', 'lastPrice', 'openInterest', 'impliedVolatility']])

    # Concatenate all data into a single DataFrame
    if options_data:
        full_data = pd.concat(options_data)
        return full_data
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data found

def save_to_csv(data, filename):
    if not data.empty:
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Define the tickers and target months
tickers = ['INTC']
target_months = ['Jun 2025', 'Jan 2026']

# Process each ticker
for ticker in tickers:
    print(f"Fetching options for {ticker}")
    options_data = fetch_options_data(ticker, target_months)
    if not options_data.empty:
        today_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"{ticker}_{today_date}.csv"
        save_to_csv(options_data, filename)
    else:
        print(f"No options data found for {ticker} in the specified months.")
