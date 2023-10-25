import os
import pandas as pd
from stock_report import *
import yfinance as yf
from datetime import datetime

# 1. CHART LINK - 캡쳐 필요
world_map_link = 'https://finviz.com/map.ashx?t=geo&st=w1'
sp500_sector_link = 'https://finviz.com/groups.ashx'
sp500_map_link = 'https://finviz.com/map.ashx?st=w1'
content1 = (f"글로벌 증시\n{world_map_link}\n"
            f"섹터별 현황\n{sp500_sector_link}\n{sp500_map_link}")

# 2.
title_tickers_dic = {}
title_tickers_dic['US Index ETF'] = ['VTI', 'VOO', 'QQQ', 'TLT']
title_tickers_dic['Dividend ETF'] = ['SCHD', 'JEPI', 'VNQ']
title_tickers_dic['S&P500'] = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'META', 'BRK-B', 'GOOG', 'UNH']
title_tickers_dic['Nasdaq'] = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'AVGO', 'TSLA', 'GOOGL', 'GOOG', 'ADBE']
title_tickers_dic['SCHD'] = ['CSCO', 'AMGN', 'ABBV', 'HD', 'AVGO', 'CVX', 'MRK', 'PEP', 'KO', 'VZ']
title_tickers_dic['VNQ'] = ['PLD', 'AMT', 'EQIX', 'CCI', 'PSA', 'O', 'SPG', 'WELL', 'DLR']

wp = WeeklyPerformanceAnalyzer()
for title, tickers in zip(title_tickers_dic.keys(), title_tickers_dic.values()):
    wp.plot_summary_charts(tickers, title, True)

# 3. News title
news_df = pd.DataFrame()
news_ticker_list = ['APPL', 'O', 'XOM']
for ticker in news_ticker_list:
    ticker_news = pd.DataFrame(yf.Ticker(ticker).news)
    ticker_news['ticker'] = ticker
    news_df = pd.concat([news_df, ticker_news])
news_df = news_df[['ticker','title','relatedTickers','link']]


# Markdown 작성
dt = datetime.now().strftime('%y%m%d')
title = f"### Weekly Report {dt}"
markdown_content = f"# {title}\n\n{content1}"

# Markdown 파일을 output 폴더에 저장
output_folder = "output"
os.makedirs(f'{output_folder}', exist_ok=True)
output_file = f"{output_folder}/{title.replace(' ', '_').lower()}.md"

with open(output_file, "w") as file:
    file.write(markdown_content)

print(f"Markdown 파일이 {output_file}에 생성되었습니다.")
