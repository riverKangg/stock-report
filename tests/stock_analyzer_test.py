import pytest
import numbers
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from stock_report.stock_analyzer import StockAnalyzer


@pytest.fixture()
def aapl_analyzer():
    return StockAnalyzer('AAPL')


@pytest.fixture()
def brkb_analyzer():
    return StockAnalyzer('BRK-B')


def essential_indices():
    return ['Share Issued', 'Net Income', 'Total Equity Gross Minority Interest', 'Total Revenue']


def test_fetch_financial_data_year_aapl(aapl_analyzer):
    fin_year_data = aapl_analyzer.fetch_financial_data(quarterly=False)
    assert len(list(filter(lambda x: x not in fin_year_data.index, essential_indices()))) == 0


def test_fetch_financial_data_year_brkb(brkb_analyzer):
    fin_year_data = brkb_analyzer.fetch_financial_data(quarterly=False)
    assert len(list(filter(lambda x: x not in fin_year_data.index, essential_indices()))) == 0


def test_fetch_financial_data_quarter_aapl(aapl_analyzer):
    fin_q_data = aapl_analyzer.fetch_financial_data(quarterly=True)
    assert len(list(filter(lambda x: x not in fin_q_data.index, essential_indices()))) == 0


def test_fetch_financial_data_quarter_brkb(brkb_analyzer):
    fin_q_data = brkb_analyzer.fetch_financial_data(quarterly=True)
    assert len(list(filter(lambda x: x not in fin_q_data.index, essential_indices()))) == 0


def test_get_closing_prices_no_input_aapl(aapl_analyzer):
    close_one = aapl_analyzer.get_closing_prices()
    assert isinstance(close_one, np.float64)


def test_get_closing_prices_with_dates_aapl(aapl_analyzer):
    before_5y = datetime.now() - timedelta(days=5 * 365)
    close_two = aapl_analyzer.get_closing_prices([before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')])
    assert isinstance(close_two, list)
    assert len(close_two) == 2
    assert len(list(filter(lambda x: not isinstance(x, float), close_two))) == 0


def test_get_dividends_no_input_aapl(aapl_analyzer):
    div_one = aapl_analyzer.get_dividends()
    assert isinstance(div_one, float)


def test_get_dividends_no_input_brkb(brkb_analyzer):
    div_one = brkb_analyzer.get_dividends()
    assert div_one == 0


def test_get_dividends_with_dates_aapl(aapl_analyzer):
    before_5y = datetime.now() - timedelta(days=5 * 365)
    dates = ['201001', before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')]
    div_two = aapl_analyzer.get_dividends(dates=dates)
    assert isinstance(div_two, list)
    assert len(div_two) == len(dates)
    assert len(list(filter(lambda x: isinstance(x, numbers.Number), div_two))) == len(dates)


def test_get_dividends_with_dates_brkb(brkb_analyzer):
    before_5y = datetime.now() - timedelta(days=5 * 365)
    dates = ['201001', before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')]
    div_two = brkb_analyzer.get_dividends(dates=dates)
    assert div_two == [0, 0, 0]


def test_last_quarter_ratios_aapl(aapl_analyzer):
    df_last = aapl_analyzer.last_quarter_ratios()
    assert df_last.shape[0] == 1
    assert df_last.columns.tolist() == ['MarketCap', 'Volume', 'CurrentPrice', '52WeekLow', '52WeekHigh', 'ROE(%)',
                                        'ROA(%)', 'OperatingProfitMargin(%)', 'NetProfitMargin(%)', 'EPS', 'PER',
                                        'PBR', 'PSR', 'PCR', 'DividendYield', 'DividendPayoutRatio']


def test_last_quarter_ratios_brkb(brkb_analyzer):
    df_last = brkb_analyzer.last_quarter_ratios()
    assert len(df_last) == 1
    assert df_last.loc[:, 'DividendYield'].values[0] == 0
    assert df_last.loc[:, 'DividendPayoutRatio'].values[0] is None


def test_annual_ratios_aapl(aapl_analyzer):
    df_finyears = aapl_analyzer.annual_ratios()
    assert df_finyears.shape[0] > 1
    assert df_finyears.columns.tolist() == ['ROE(%)', 'ROA(%)', 'OperatingProfitMargin(%)', 'NetProfitMargin(%)', 'EPS',
                                            'PER', 'PBR', 'PSR', 'PCR', 'DividendYield', 'DividendPayoutRatio']
    assert len(list(filter(lambda x: isinstance(x, numbers.Number), df_finyears.iloc[0]))) == df_finyears.shape[1]


def test_annual_ratios_brkb(brkb_analyzer):
    df_finyears = brkb_analyzer.annual_ratios()
    assert sum(df_finyears.loc[:, 'DividendYield']) == 0
    assert df_finyears.loc[:, 'DividendPayoutRatio'].tolist() == [None] * df_finyears.shape[0]


def test_fetch_financial_data_aapl(aapl_analyzer):
    df_yearly = aapl_analyzer.fetch_financial_data()
    assert df_yearly.shape[0] > 0 and df_yearly.shape[1] == 4


# def test_get_financial_data_period_brkb(brkb_analyzer):
#     start_date = '202201'
#     end_date = '202303'
#     df = brkb_analyzer.get_financial_data_period(start_date, end_date)
#     assert df is not None
#     assert df.shape[0] > 0
#     assert all(start_date <= df.index) and all(df.index <= end_date)
#
#
# def test_get_closing_prices_period_aapl(aapl_analyzer):
#     start_date = '202201'
#     end_date = '202303'
#     closing_prices = aapl_analyzer.get_closing_prices_period(start_date, end_date)
#     assert closing_prices is not None
#     assert isinstance(closing_prices, pd.Series)
#     assert all(start_date <= closing_prices.index) and all(closing_prices.index <= end_date)
#
#
# def test_get_closing_prices_period_brkb(brkb_analyzer):
#     start_date = '202201'
#     end_date = '202303'
#     closing_prices = brkb_analyzer.get_closing_prices_period(start_date, end_date)
#     assert closing_prices is not None
#     assert isinstance(closing_prices, pd.Series)
#     assert all(start_date <= closing_prices.index) and all(closing_prices.index <= end_date)
#
#
# def test_get_dividends_period_aapl(aapl_analyzer):
#     start_date = '202201'
#     end_date = '202303'
#     dividends = aapl_analyzer.get_dividends_period(start_date, end_date)
#     assert dividends is not None
#     assert isinstance(dividends, pd.Series)
#     assert all(start_date <= dividends.index) and all(dividends.index <= end_date)
#
#
# def test_get_dividends_period_brkb(brkb_analyzer):
#     start_date = '202201'
#     end_date = '202303'
#     dividends = brkb_analyzer.get_dividends_period(start_date, end_date)
#     assert dividends is not None
#     assert isinstance(dividends, pd.Series)
#     assert all(start_date <= dividends.index) and all(dividends.index <= end_date)
