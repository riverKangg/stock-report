import pytest
from stock_report.get_sp500_list import getSp500List


@pytest.fixture()
def sp():
    return getSp500List()

def test_get_data(sp):
    data = sp.get_data()
    assert data.columns.tolist() == ['Name', 'Sector', 'Industry']


def test_from_wiki(sp):
    wiki_data = sp.from_wiki()
    assert wiki_data.columns.tolist() == ['Security', 'GICS Sector', 'GICS Sub-Industry',
                                          'Headquarters Location', 'Date added', 'CIK', 'Founded']

def test_number(sp):
    data = sp.get_data()
    wiki_data = sp.from_wiki()
    assert data.shape[0] == wiki_data.shape[0]