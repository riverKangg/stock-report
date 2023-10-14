import warnings
import pandas as pd
import os
from stock_report.sp500_list_fetcher import SP500ListFetcher
from stock_report.stock_analyzer import StockAnalyzer

warnings.filterwarnings('ignore')

def analyze_sp500_stocks(save_dir):
    # Step 1: Get S&P 500 tickers
    sp500_data = SP500ListFetcher().get_sp500_data()
    sp500_tickers = sp500_data.index.tolist()

    # Step 2: Analyze S&P 500 stocks
    data = {}
    for ticker in sp500_tickers:
        mr = StockAnalyzer(ticker)
        data[ticker] = mr.last_quarter_ratios().iloc[0]

    # Step 3: Sort by PER in descending order
    df_valuation = pd.DataFrame(data).T.sort_values(by='PER', ascending=False)

    # Step 4: Save the data to a CSV file
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'sp500_valuation_data.csv')
    df_valuation.to_csv(save_path)

    return df_valuation

if __name__ == "__main__":
    save_directory = "sp500_data"
    analyzed_data = analyze_sp500_stocks(save_directory)
    print(analyzed_data.shape)
