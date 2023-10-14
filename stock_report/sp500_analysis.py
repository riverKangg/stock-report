import os
import pandas as pd
import warnings
from stock_report.sp500_list_fetcher import SP500ListFetcher
from stock_report.stock_analyzer import StockAnalyzer
from numerize import numerize

warnings.filterwarnings('ignore')

def analyze_or_load_sp500_data(save_directory):
    data_file_path = os.path.join(save_directory, 'sp500_valuation_data.csv')

    # Check if the data file already exists
    if os.path.exists(data_file_path):
        # Load and return the existing data
        valuation_data = pd.read_csv(data_file_path, index_col=0)
        return valuation_data

    # Step 1: Get S&P 500 tickers
    sp500_data = SP500ListFetcher().get_sp500_data()
    sp500_tickers = sp500_data.index.tolist()

    # Step 2: Analyze S&P 500 stocks
    analyzed_data = {}
    error_tickers = []  # 에러가 발생한 티커 목록

    for ticker in sp500_tickers:
        try:
            stock_analyzer = StockAnalyzer(ticker)
            analyzed_data[ticker] = stock_analyzer.last_quarter_ratios().iloc[0]
        except Exception as e:
            error_tickers.append(ticker)
            print(f"Error analyzing {ticker}: {str(e)}")

    for error_ticker in error_tickers:
        sp500_tickers.remove(error_ticker)  # 에러 티커 제외

    # Step 3: Sort by PER in descending order
    valuation_data = pd.DataFrame(analyzed_data).T

    # Step 4: Save the data to a CSV file
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    valuation_data.to_csv(data_file_path)

    return valuation_data

def get_top_10_market_cap_stocks(valuation_data):
    if valuation_data is not None:
        if 'MarketCap' in valuation_data.columns:
            top_10_market_cap = valuation_data.sort_values(by='MarketCap', ascending=False).head(10)
            return top_10_market_cap
        else:
            print("Column 'MarketCap' not found in the data.")
    else:
        print("Data file not found in the specified directory.")

    return None

if __name__ == "__main__":
    save_directory = "sp500_data"

    # Analyze S&P 500 stocks and save the data if not already saved
    analyzed_data = analyze_or_load_sp500_data(save_directory)
    if analyzed_data is not None:
        print(analyzed_data.shape)

    # Get the top 10 stocks by MarketCap (in original format, no Large Number Abbreviations)
    top_10_market_cap_stocks = get_top_10_market_cap_stocks(analyzed_data)

    if top_10_market_cap_stocks is not None:
        print(top_10_market_cap_stocks)
