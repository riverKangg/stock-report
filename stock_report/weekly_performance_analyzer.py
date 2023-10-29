# -*- coding: utf-8 -*-
import os
import warnings
import pandas as pd
from datetime import datetime
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')


class WeeklyPerformanceAnalyzer:
    def __init__(self, start_year='2018'):
        self.start_year = start_year
        self.TODAY = datetime.now().strftime('%y%m%d')
        self.OUTPUT_PATH = './output/'
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)

    def fetch_stock_data(self, ticker):
        """
        This function retrieves stock data.

        :param ticker: string
            The symbol of the stock (e.g., 'AAPL' for Apple stock).
        :return: dataframe
            Returns a dataframe containing stock data.
        """
        stock_data = fdr.DataReader(symbol=ticker, start=self.start_year).reset_index()
        return stock_data

    def generate_weekly_data(self, ticker):
        """
        Generate weekly_graph stock data based on the last date of each week.

        :param ticker: string
            The symbol of the stock (e.g., 'AAPL' for Apple stock).
        :return: dataframe
            Returns a dataframe containing stock data with only the last date of each week.
        """
        daily_data = self.fetch_stock_data(ticker)
        weekly_last_dates = daily_data.groupby(daily_data['Date'].dt.strftime('%Y-%U'))['Date'].max()
        weekly_data = daily_data[daily_data['Date'].isin(weekly_last_dates)]
        return weekly_data

    def generate_summary_values(self, df):
        max_value = max(df.Close)
        last_value = list(df.Close)[-2]
        current_value = list(df.Close)[-1]
        decline_rate_from_last = (current_value - last_value) / last_value * 100
        decline_rate_from_max = round((current_value - max_value) / max_value * 100, 1)
        return [current_value, decline_rate_from_last, max_value, decline_rate_from_max]

    def generate_summary_table(self, ticker_list):
        """
        Generate a summary table for a list of stock tickers based on weekly_graph data.

        :param ticker_list: list
            A list of stock ticker symbols (e.g., ['AAPL', 'GOOGL']).
        :return: dataframe
            Returns a summary table as a Pandas DataFrame containing information for each stock.
        """
        summary_data = []

        for ticker in ticker_list:
            raw_data = self.fetch_stock_data(ticker)
            weekly_data = self.generate_weekly_data(ticker)
            summary_values = [ticker] + self.generate_summary_values(weekly_data)
            summary_data.append(summary_values)

        summary_table = pd.DataFrame(summary_data,
                                     columns=['Ticker', 'Current', 'LastWeekChange', 'High', 'HighChange'])

        print(f'★ {ticker_list}')
        print(summary_table)
        print('')
        return summary_table

    def plot_summary_charts(self, ticker_list, title, file_path=None, return_table=False):
        ticker_list.reverse()
        df_summary = self.generate_summary_table(ticker_list)

        width = len(ticker_list) * 0.8 if len(ticker_list) < 5 else len(ticker_list) * 0.4
        fig = plt.figure(figsize=(13, width))

        ax1 = fig.add_subplot(1, 2, 1)
        indexes, values = df_summary.Ticker, list(map(lambda x: round(x, 2), df_summary.LastWeekChange))
        bars = ax1.barh(indexes, values, height=0.6, color='lightsteelblue')
        ax1.bar_label(bars, padding=-32, color='white', fontweight='900')
        ax1.set_title(f'[{title}] Last Week Change')

        ax2 = fig.add_subplot(1, 2, 2)
        indexes, values = df_summary.Ticker, list(map(lambda x: round(x, 2), df_summary.HighChange))
        bars = ax2.barh(indexes, values, height=0.6, color='lightcoral')
        ax2.bar_label(bars, padding=-32, color='white', fontweight='900')
        ax2.set_title(f'[{title}] High Point Change')

        save_title = title.replace(' ', '')
        if file_path:
            plt.savefig(f'{file_path}/{save_title}_{self.TODAY}.jpg')
        else:
            plt.savefig(f'{self.OUTPUT_PATH}/{save_title}_{self.TODAY}.jpg')

        if return_table:
            return df_summary

    # --- Closing Price Trends
    def generate_close_table(self, ticker_list):
        df_close = pd.DataFrame()
        for ticker in ticker_list:
            raw_data = fdr.DataReader(ticker, self.start_year).reset_index()
            data = self.generate_weekly_data(raw_data)
            if len(df_close) == 0:
                df_close['date'] = data.Date
            df_close[ticker] = data.Close
        df_close = df_close.set_index('date')
        return df_close

    # --- Comparison of Rise Rates
    def generate_rise_table(self, ticker_list):
        # Data for comparing rise rates over a certain period
        df_rise = pd.DataFrame()
        for ticker in ticker_list:
            raw_data = fdr.DataReader(ticker, self.start_year).reset_index()
            data = self.generate_weekly_data(raw_data)
            if len(df_rise) == 0:
                df_rise['date'] = data.Date
            rise_list = []
            first_value = data.Close[0]
            for i in range(len(data)):
                one_week_rise = (data.Close[i] - first_value) / first_value * 100
                rise_list += [one_week_rise]
            df_rise[ticker] = rise_list
        df_rise = df_rise.set_index('date')
        return df_rise

    def plot_rise_chart(self, ticker_list):
        plt_df = self.generate_rise_table(ticker_list)

        plt.figure(figsize=(5, 3))

        for ticker in plt_df.columns:
            var = plt_df[ticker]
            plt.plot(var)
            plt.annotate(f'{ticker}  {var[-1]:0.1f}%', xy=(1, var[-1]), xytext=(8, 0),
                         xycoords=('axes fraction', 'data'), textcoords='offset points')
        plt.legend(plt_df.columns)
        plt.show()


if __name__ == '__main__':
    wp = WeeklyPerformanceAnalyzer()
    wp.plot_summary_charts(['VTI', 'VOO', 'QQQ', 'TLT'], 'US Index ETF')
