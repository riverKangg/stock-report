import pytest
from stock_report.get_sp500_list import getSp500List

@pytest.fixture()
def sp():
    return getSp500List()

def test_get_base_data(sp):
    data = sp.get_base_data()
    assert data.columns.tolist() == ['Name', 'Sector', 'Industry']

def test_get_data_from_wiki(sp):
    wiki_data = sp.get_data_from_wiki()
    assert wiki_data.columns.tolist() == ['Security', 'GICS Sector', 'GICS Sub-Industry',
                                          'Headquarters Location', 'Date added', 'CIK', 'Founded']

def test_symbol_count(sp):
    data = sp.get_base_data()
    wiki_data = sp.get_data_from_wiki()
    assert data.shape[1] == wiki_data.shape[1]

