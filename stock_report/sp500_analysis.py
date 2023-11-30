import os
import warnings
import pandas as pd
from tqdm import tqdm
from numerize import numerize
from stock_report.stock_analyzer import StockAnalyzer
from stock_report.sp500_list_fetcher import SP500ListFetcher
from utils import *

warnings.filterwarnings('ignore')

def fetch_or_load_sp500_data(save_directory):
    data_file_path = os.path.join(save_directory, 'sp500_valuation_data.csv')

    # Check if the data file already exists
    if os.path.exists(data_file_path):
        # Load and return the existing data
        valuation_data = pd.read_csv(data_file_path, index_col=0)
        return valuation_data

    # Step 1: Get S&P 500 tickers
    print('Start Fetching')
    sp500_data = SP500ListFetcher().get_sp500_data()
    sp500_tickers = sp500_data.index.tolist()

    # Step 2: Fetch S&P 500 stocks
    analyzed_data = {}
    error_tickers = []  # 에러가 발생한 티커 목록

    for ticker in tqdm(sp500_tickers):
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

def add_sp500_info(valuation_data):
    sp500_data = SP500ListFetcher().get_sp500_data()
    valuation_data = valuation_data.join(sp500_data)
    return valuation_data

def save_top_stocks_to_csv(top_stocks, metric, save_directory, group_by=None):
    if group_by:
        csv_file_name = f'top_{metric}_{group_by}.csv'
    else:
        csv_file_name = f'top_{metric}.csv'

    csv_file_path = os.path.join(save_directory, csv_file_name)
    top_stocks.to_csv(csv_file_path, sep="\t", index=False)


def save_grouped_data_to_csv(grouped_data, metric, save_directory):
    csv_file_name = f'GRP_{metric}.csv'
    csv_file_path = os.path.join(save_directory, csv_file_name)
    grouped_data.to_csv(csv_file_path, sep="\t")


def get_top_n_stocks(valuation_data, metric, n=10, ascending=True, group_by=None):
    if metric not in valuation_data.columns:
        print(f"Column '{metric}' not found in the data.")
        return None

    valuation_data[metric] = pd.to_numeric(valuation_data[metric], errors='coerce')


    if group_by:
        valuation_data = add_sp500_info(valuation_data)
        valuation_data = valuation_data[valuation_data[metric]>0]
        top_stocks = valuation_data.groupby(group_by).apply(lambda x: x.nsmallest(n, metric))[[metric,'MarketCap']].reset_index()
        top_stocks.columns = [group_by, 'Symbol', metric, 'MarketCap']
        top_stocks[metric] = top_stocks[metric].apply(lambda x: round(x, 1))
        top_stocks['MarketCap'] = top_stocks['MarketCap'].apply(lambda x: numerize.numerize(x))

        # Calculating the Number of Companies and Average Metric by Sector.
        grouped_data = valuation_data.groupby(group_by)[metric].agg(['count', 'mean'])
        grouped_data = grouped_data.sort_values(by='mean')
        grouped_data['mean'] = grouped_data['mean'].apply(lambda x: round(x, 1))
        save_grouped_data_to_csv(grouped_data, metric, save_directory)

    else:
        top_stocks = valuation_data.nlargest(n, metric)[[metric]]
        top_stocks[metric] = top_stocks[metric].apply(lambda x: numerize.numerize(x))
        top_stocks = top_stocks.reset_index()
        top_stocks.columns = ['Symbol', metric]

    return top_stocks


if __name__ == "__main__":
    root_dir = get_git_root_directory()
    save_directory = f"{root_dir}/output/sp500"

    analyzed_data = fetch_or_load_sp500_data(save_directory)

    if analyzed_data is not None:
        print(analyzed_data.shape)

        # Get the top 10 MarketCap stocks and save to CSV:
        top_10_market_cap_stocks = get_top_n_stocks(analyzed_data, 'MarketCap', n=10, ascending=False)
        save_top_stocks_to_csv(top_10_market_cap_stocks, 'MarketCap', save_directory)

        # Get the top 10 PER Sector and save to CSV:
        top_10_per_sector = get_top_n_stocks(analyzed_data, 'PER', n=5, ascending=True, group_by='Sector')
        save_top_stocks_to_csv(top_10_per_sector, 'PER', save_directory, 'Sector')

        # Get the top 10 PBR Sector and save to CSV:
        top_10_pbr_sector = get_top_n_stocks(analyzed_data, 'PBR', n=5, ascending=True, group_by='Sector')
        save_top_stocks_to_csv(top_10_pbr_sector, 'PBR', save_directory, 'Sector')
