import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_options_data(tickers):
    all_options = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        print(f"Fetching options for {ticker}")
        # Attempt to get options data if available
        try:
            exp_dates = stock.options
            for date in exp_dates:
                opts = stock.option_chain(date)
                data = pd.concat([opts.calls, opts.puts])
                data['Ticker'] = ticker
                data['Expiration Date'] = date
                all_options.append(data)
        except Exception as e:
            print(f"Could not fetch options for {ticker}: {e}")
    
    # Combine all options into a single DataFrame
    if all_options:
        return pd.concat(all_options, ignore_index=True)
    else:
        return pd.DataFrame()

def main():
    # List of top market cap company tickers
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
    options_data = fetch_options_data(tickers)
    
    if not options_data.empty:
        # Format today's date as YYYY-MM-DD
        today_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"options_data_{today_date}.csv"
        options_data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No options data fetched.")

if __name__ == "__main__":
    main()
