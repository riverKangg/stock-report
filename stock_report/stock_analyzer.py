import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class StockAnalyzer:

    def __init__(self, ticker):
        self.ticker = ticker
        self.val_df = pd.DataFrame()

    def fetch_financial_data(self, quarterly=False):
        tic = yf.Ticker(self.ticker)
        if quarterly:
            tic_fin = pd.concat([tic.quarterly_income_stmt, tic.quarterly_balance_sheet, tic.quarterly_cashflow])
        else:
            tic_fin = pd.concat([tic.income_stmt, tic.balance_sheet, tic.cashflow])
        tic_fin.columns = list(map(lambda x: x.strftime('%Y%m'), tic_fin.columns))
        return tic_fin

    def get_closing_prices(self, dates=[]):
        tic_hist = yf.Ticker(self.ticker).history(period='5y')
        tic_hist.index = list(map(lambda x: x.strftime('%Y%m'), tic_hist.index))
        if not dates:
            close = tic_hist.Close[-1]
        else:
            tic_hist = tic_hist.reset_index().groupby('index').last()
            close = tic_hist.loc[dates].Close.tolist()
        return close

    def get_dividends(self, dates=[]):
        tic_div = yf.Ticker(self.ticker).dividends.to_frame()
        tic_div.index = list(map(lambda x: x.strftime('%Y%m'), tic_div.index))
        if not dates:
            today = datetime.today().strftime('%Y%m')
            before1y = (datetime.today() - timedelta(days=365)).strftime('%Y%m')
            tic_div = tic_div.loc[filter(lambda x: (x <= today) & (x >= before1y), tic_div.index)]
            div = sum(tic_div.Dividends)
        else:
            dates_before1y = list(map(lambda x: pd.to_numeric(x) - 100, dates))
            div = []
            for start, end in zip(dates_before1y, dates):
                start = str(start)
                end = str(end)
                tic_div1y = tic_div.loc[filter(lambda x: (start <= x) & (x <= end), tic_div.index)]
                div += [sum(tic_div1y.Dividends)]
        return div

    # --- ADD INFO
    def add_info(self, df):
        info_data = yf.Ticker(self.ticker).info
        self.val_df['MarketCap'] = df.loc['marketCap']
        self.val_df['Volume'] = info_data['volume']
        self.val_df['CurrentPrice'] = df.loc['Close'].apply(lambda x: round(x, 3))
        self.val_df['52WeekLow'] = info_data['fiftyTwoWeekLow']
        self.val_df['52WeekHigh'] = info_data['fiftyTwoWeekHigh']

    # --- ADD RATIOS
    def add_profitability_ratios(self, df):
        self.val_df['ROE(%)'] = (df.loc['Net Income'] / df.loc['Total Equity Gross Minority Interest']) * 100
        self.val_df['ROA(%)'] = (df.loc['Net Income'] / df.loc['Total Assets']) * 100
        if 'Operating Income' in self.idx:
            self.val_df['OperatingProfitMargin(%)'] = (df.loc['Operating Income'] / df.loc['Total Revenue']) * 100
            self.val_df['NetProfitMargin(%)'] = (df.loc['Operating Income'] / df.loc['Net Income']) * 100
        else:
            self.val_df['OperatingProfitMargin(%)'] = None
            self.val_df['NetProfitMargin(%)'] = None

    def add_value_ratios(self, df):
        self.val_df['EPS'] = df.loc['Net Income'] / df.loc['Share Issued']
        self.val_df['PER'] = df.loc['marketCap'] / df.loc['Net Income']
        self.val_df['PBR'] = df.loc['marketCap'] / df.loc['Total Equity Gross Minority Interest']
        self.val_df['PSR'] = df.loc['marketCap'] / df.loc['Total Revenue']
        self.val_df['PCR'] = df.loc['marketCap'] / df.loc['Operating Cash Flow']

    def add_dividend_ratios(self, df):
        self.val_df['DividendYield'] = df.loc['Dividends'] / df.loc['Close']
        if 'Cash Dividends Paid' in self.idx:
            self.val_df['DividendPayoutRatio'] = df.loc['Cash Dividends Paid'] / df.loc['Net Income']
        else:
            self.val_df['DividendPayoutRatio'] = None

    # --- SHOW REPORT
    def last_quarter_ratios(self):
        self.val_df = self.val_df.loc[0:0]

        df = self.fetch_financial_data(quarterly=True)
        self.idx = list(df.index)
        if 'Net Income' not in self.idx:
            df = self.fetch_financial_data()
            self.idx = list(df.index)
        max_date = max(df.columns)
        df = df[[max_date]]

        df.loc['Close'] = self.get_closing_prices()
        df.loc['Dividends'] = self.get_dividends()
        df.loc['marketCap'] = df.loc['Close'] * df.loc['Share Issued']

        self.add_info(df)
        self.add_profitability_ratios(df)
        self.add_value_ratios(df)
        self.add_dividend_ratios(df)

        return self.val_df

    def annual_ratios(self):
        self.val_df = self.val_df.loc[0:0]

        df = self.fetch_financial_data(quarterly=False)
        self.idx = list(df.index)
        basedates = list(df.columns)

        df.loc['Close'] = self.get_closing_prices(basedates)
        df.loc['Dividends'] = self.get_dividends(basedates)
        df.loc['marketCap'] = df.loc['Close'] * df.loc['Share Issued']

        self.add_profitability_ratios(df)
        self.add_value_ratios(df)
        self.add_dividend_ratios(df)

        return self.val_df
