import numpy as np
import pytest
import numbers
from datetime import datetime, timedelta
from stock_report.add_indicator import addIndicator

@pytest.fixture()
def ai_aapl():
    return addIndicator('AAPL')
@pytest.fixture()
def ai_brkb():
    return addIndicator('BRK-B')

def essential_index():
    return ['Share Issued', 'Net Income', 'Total Equity Gross Minority Interest', 'Total Revenue']

def test_df_financials_year_appl(ai_aapl):
    fin_year_data = ai_aapl.df_financials_year()
    assert len(list(filter(lambda x: x not in fin_year_data.index, essential_index()))) == 0

def test_df_financials_year_brkb(ai_brkb):
    fin_year_data = ai_brkb.df_financials_year()
    assert len(list(filter(lambda x: x not in fin_year_data.index, essential_index()))) == 0

def test_df_financials_quater_aapl(ai_aapl):
    fin_q_data = ai_aapl.df_financials_quarter()
    assert len(list(filter(lambda x: x not in fin_q_data.index, essential_index()))) == 0

def test_df_financials_quater_brkb(ai_brkb):
    fin_q_data = ai_brkb.df_financials_quarter()
    assert len(list(filter(lambda x: x not in fin_q_data.index, essential_index()))) == 0

def test_data_close_noinput_aapl(ai_aapl):
    close_one = ai_aapl.data_close()
    assert type(close_one) == np.float64

def test_data_close_dates_aapl(ai_aapl):
    before_5y = datetime.now() - timedelta(days=5*365)
    close_two = ai_aapl.data_close(dates=[before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')])
    assert type(close_two) == list
    assert len(close_two) == 2
    assert len(list(filter(lambda x: type(x)!=float, close_two))) == 0

def test_data_div_noinput_aapl(ai_aapl):
    div_one = ai_aapl.data_div()
    assert type(div_one) == float

def test_data_div_noinput_brkb(ai_brkb):
    div_one = ai_brkb.data_div()
    assert div_one == 0

def test_data_div_dates_aapl(ai_aapl):
    before_5y = datetime.now() - timedelta(days=5*365)
    dates = ['201001', before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')]
    div_two = ai_aapl.data_div(dates=dates)
    print(div_two)
    assert type(div_two) == list
    assert len(div_two) == len(dates)
    assert len(list(filter(lambda x: isinstance(x, numbers.Number), div_two))) == len(dates)

def test_data_div_dates_brkb(ai_brkb):
    before_5y = datetime.now() - timedelta(days=5*365)
    dates = ['201001', before_5y.strftime('%Y%m'), datetime.now().strftime('%Y%m')]
    div_two = ai_brkb.data_div(dates=dates)
    assert div_two == [0, 0, 0]

def test_ratio_last_aapl(ai_aapl):
    df_last = ai_aapl.ratio_last()
    assert df_last.shape[0] == 1
    assert df_last.columns.tolist() == ['시가총액', '거래량', '현재가', '52주저가', '52주고가', 'ROE(%)', 'ROA(%)',
                                        '영업이익률(%)', '당기순이익률(%)', 'EPS', 'PER', 'PBR', 'PSR', 'PCR',
                                        '배당수익률', '배당성향']

def test_ratio_last_brkb(ai_brkb):
    df_last = ai_brkb.ratio_last()
    assert df_last.loc[:, '배당수익률'].values == 0
    assert df_last.loc[:, '배당성향'].values == None
