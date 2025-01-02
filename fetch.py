import yfinance as yf
from datetime import datetime, timedelta

def fetch_options(ticker):
    # Fetch the data for the given ticker
    stock = yf.Ticker(ticker)
    
    # Get the current stock price
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    
    # Get options expirations
    expirations = stock.options
    
    # Calculate the next three months range
    three_months = [exp for exp in expirations if datetime.strptime(exp, "%Y-%m-%d") <= datetime.now() + timedelta(days=90)]
    
    options_data = {
        "calls": [],
        "puts": []
    }
    
    # Fetch the option chain for the next three months
    for exp in three_months:
        opt = stock.option_chain(exp)
        
        # Get three closest call options
        calls = opt.calls
        calls['distance'] = abs(calls['strike'] - current_price)
        closest_calls = calls.sort_values(by='distance').head(3)[['strike', 'lastPrice', 'distance']]
        
        # Get three closest put options
        puts = opt.puts
        puts['distance'] = abs(puts['strike'] - current_price)
        closest_puts = puts.sort_values(by='distance').head(3)[['strike', 'lastPrice', 'distance']]
        
        options_data['calls'].append(closest_calls)
        options_data['puts'].append(closest_puts)
    
    return options_data

# Tickers to fetch options for
tickers = ["INTC", "CLF", "MSTR"]

# Get options data for each ticker
all_data = {}
for ticker in tickers:
    print(f"Fetching options for {ticker}")
    all_data[ticker] = fetch_options(ticker)
    print(f"Options for {ticker}: Calls - {all_data[ticker]['calls']} Puts - {all_data[ticker]['puts']}")
