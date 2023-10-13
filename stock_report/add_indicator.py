import numpy as np
import pandas as pd
import yfinance as yf
from numerize import numerize
from datetime import datetime, timedelta


class addIndicator:
    def __init__(self, ticker):
        self.ticker = ticker
        self.val_df = pd.DataFrame()

    # --- READ DATA
    def df_financials_year(self):
        # 재무제표 데이터
        tic = yf.Ticker(self.ticker)
        tic_fin = pd.concat([tic.income_stmt, tic.balance_sheet, tic.cashflow])
        tic_fin.columns = list(map(lambda x: x.strftime('%Y%m'), tic_fin.columns))
        return tic_fin

    def df_financials_quarter(self):
        # 분기 재무제표 데이터
        tic = yf.Ticker(self.ticker)
        tic_fin = pd.concat([tic.quarterly_income_stmt, tic.quarterly_balance_sheet, tic.quarterly_cashflow])
        tic_fin.columns = list(map(lambda x: x.strftime('%Y%m'), tic_fin.columns))
        return tic_fin

    def data_close(self, dates=[]):
        """
        :param dates: list
            values consisting of the format 'YYYYMM'
            e.g. ['202201', '202310']
        :return: float or list
            values consisting of the monthly closing price
            If there is no input, return last close value
        """
        tic_hist = yf.Ticker(self.ticker).history(period='5y')
        tic_hist.index = list(map(lambda x: x.strftime('%Y%m'), tic_hist.index))
        if dates == []:
            close = tic_hist.Close[-1]
        else:
            tic_hist = tic_hist.reset_index().groupby('index').last()
            close = tic_hist.loc[dates].Close.tolist()
        return close

    def data_div(self, dates=[]):
        """
        :param dates:
        :return: float or list
            If there is no input, return sum of dividends in the past year
        """
        tic_div = yf.Ticker(self.ticker).dividends.to_frame()
        tic_div.index = list(map(lambda x: x.strftime('%Y%m'), tic_div.index))
        if dates == []:
            today = datetime.today().strftime('%Y%m')
            before1y = datetime.today() - timedelta(days=365)
            before1y = before1y.strftime('%Y%m')
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
        self.val_df['시가총액'] = df.loc['marketCap'].apply(lambda x: numerize.numerize(x))
        self.val_df['거래량'] = numerize.numerize(info_data['volume'])
        self.val_df['현재가'] = df.loc['Close'].apply(lambda x: round(x, 3))
        self.val_df['52주저가'] = info_data['fiftyTwoWeekLow']
        self.val_df['52주고가'] = info_data['fiftyTwoWeekHigh']

    # --- ADD RATIO
    def add_profitability(self, df):
        # 수익성 지표
        self.val_df['ROE(%)'] = df.loc['Net Income'] / df.loc['Total Equity Gross Minority Interest'] * 100
        self.val_df['ROA(%)'] = df.loc['Net Income'] / df.loc['Total Assets'] * 100
        if 'Operating Income' in self.idx:
            self.val_df['영업이익률(%)'] = df.loc['Operating Income'] / df.loc['Total Revenue'] * 100
            self.val_df['당기순이익률(%)'] = df.loc['Operating Income'] / df.loc['Net Income'] * 100
        else:
            self.val_df['영업이익률(%)'] = None
            self.val_df['당기순이익률(%)'] = None

    def add_value(self, df):
        # 가치 지표
        self.val_df['EPS'] = df.loc['Net Income'] / df.loc['Share Issued']

        self.val_df['PER'] = df.loc['marketCap'] / df.loc['Net Income']
        self.val_df['PBR'] = df.loc['marketCap'] / df.loc['Total Equity Gross Minority Interest']
        self.val_df['PSR'] = df.loc['marketCap'] / df.loc['Total Revenue']
        self.val_df['PCR'] = df.loc['marketCap'] / df.loc['Operating Cash Flow']

    def add_div(self, df):
        # 배당 지표
        self.val_df['배당수익률'] = df.loc['Dividends'] / df.loc['Close']
        if 'Cash Dividends Paid' in self.idx:
            self.val_df['배당성향'] = df.loc['Cash Dividends Paid'] / df.loc['Net Income']
        else:
            self.val_df['배당성향'] = None

    # --- SHOW REPORT
    def ratio_last(self):
        self.val_df = self.val_df.loc[0:0]

        df = self.df_financials_quarter()
        self.idx = list(df.index)
        if 'Net Income' not in self.idx:
            df = self.df_financials()
            self.idx = list(df.index)
        max_date = max(df.columns)
        df = df[[max_date]]

        df.loc['Close'] = self.data_close()
        df.loc['Dividends'] = self.data_div()
        df.loc['marketCap'] = df.loc['Close'] * df.loc['Share Issued']

        self.add_info(df)
        self.add_profitability(df)
        self.add_value(df)
        self.add_div(df)

        return self.val_df

    def ratio_finYear(self):
        self.val_df = self.val_df.loc[0:0]

        df = self.df_financials_year()
        self.idx = list(df.index)
        basedates = list(df.columns)

        df.loc['Close'] = self.data_close(basedates)
        df.loc['Dividends'] = self.data_div(basedates)
        df.loc['marketCap'] = df.loc['Close'] * df.loc['Share Issued']

        self.add_profitability(df)
        self.add_value(df)
        self.add_div(df)

        return self.val_df