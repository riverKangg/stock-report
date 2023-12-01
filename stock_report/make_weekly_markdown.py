import os
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from datetime import datetime

from utils import *

dt = datetime.now().strftime('%y%m%d')
report_path = '/Users/samsung/PycharmProjects/stock-report/output/weekly/'
graph_path = f'{report_path}/graph/{dt}/'
os.makedirs(report_path, exist_ok=True)
os.makedirs(graph_path, exist_ok=True)

content = f"# Weekly Report {dt}\n\n"

# 1. CHART LINK - 캡쳐 필요
content += '## 1. 글로벌, 섹터별 맵\n'
content += "- 글로벌 증시: [글로벌맵](https://finviz.com/map.ashx?t=geo&st=w1)\n"
content += "- 섹터별 현황: [섹터별차트](https://finviz.com/groups.ashx), [섹터별맵](https://finviz.com/map.ashx?st=w1)"
content += '\n---\n'

# 2. 주요 ETF 그래프
wp = WeeklyPerformanceAnalyzer()

content += "## 2. 주요 ETF 현황\n"
content += "### 2-1. 미국 지수 ETF\n"
title, tickers = 'US Index ETF', ['VTI', 'VOO'] #, 'QQQ', 'TLT'
df_summery = wp.plot_summary_charts(tickers, title, graph_path, True)
content += f"![미국지수그래프]({graph_path}/USIndexETF_{dt}.jpg)\n\n"
content += df_summery.to_markdown(index=False)

# title_tickers_dic1['Dividend ETF'] = ['SCHD', 'JEPI', 'VNQ']
# for title, tickers in zip(title_tickers_dic1.keys(), title_tickers_dic1.values()):
#
#
# title_tickers_dic['S&P500'] = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'META', 'BRK-B', 'GOOG', 'UNH']
# title_tickers_dic['Nasdaq'] = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'AVGO', 'TSLA', 'GOOGL', 'GOOG', 'ADBE']
# title_tickers_dic['SCHD'] = ['CSCO', 'AMGN', 'ABBV', 'HD', 'AVGO', 'CVX', 'MRK', 'PEP', 'KO', 'VZ']
# title_tickers_dic['VNQ'] = ['PLD', 'AMT', 'EQIX', 'CCI', 'PSA', 'O', 'SPG', 'WELL', 'DLR']
#
#
#
# content += (
#             f"### 2-2. 주요 배당 ETF\n"
#             f"![graph]({graph_path}/DividendETF_{dt}.jpg)\n\n")
# content += '\n---'
#
# content += ("## 3. 주요 기업 현황\n"
#             "### 3-1. S&P500 주요 기업\n"
#             f"![graph]({graph_path}/S&P500_{dt}.jpg)\n"
#             f"### 3-2. 나스닥 주요 기업\n"
#             f"![graph]({graph_path}/Nasdaq_{dt}.jpg)\n"
#             f"### 3-3. SCHD 주요 기업\n"
#             f"![graph]({graph_path}/SCHD_{dt}.jpg)\n"
#             f"### 3-4. VNQ 주요 기업\n"
#             f"![graph]({graph_path}/VNQ_{dt}.jpg)\n")
content += '\n\n---\n'

# 3. News title
# news_df = pd.DataFrame()
# news_ticker_list = ['APPL', 'O', 'XOM']
# for ticker in news_ticker_list:
#     ticker_news = pd.DataFrame(yf.Ticker(ticker).news)
#     ticker_news['ticker'] = ticker
#     news_df = pd.concat([news_df, ticker_news])
# news_df = news_df[['ticker', 'title', 'relatedTickers', 'link']]
content += "### 4. 기업별 주요 뉴스"
content += '\n\n---\n'


# Markdown 작성
with open(f'{report_path}/weekly_report_{dt}.md', "w") as f:
    f.write(content)
