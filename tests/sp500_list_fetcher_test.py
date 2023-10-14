import pytest
from stock_report.sp500_list_fetcher import SP500ListFetcher


@pytest.fixture()
def sp():
    return SP500ListFetcher()


def test_get_base_data(sp):
    data = sp.get_base_data()
    assert data.columns.tolist() == ['Name', 'Sector', 'Industry']

    # Additional validations
    assert data.shape[0] > 0  # Check if there are rows
    assert all(data['Symbol'].str.isalpha())  # Check if 'Symbol' contains only alphabetic characters
    assert all(data['Name'].notnull())  # Check if 'Name' does not contain missing values
    assert all(data['Sector'].notnull())  # Check if 'Sector' does not contain missing values
    assert all(data['Industry'].notnull())  # Check if 'Industry' does not contain missing values


def test_get_data_from_wiki(sp):
    wiki_data = sp.get_data_from_wiki()
    assert wiki_data.columns.tolist() == ['Security', 'GICS Sector', 'GICS Sub-Industry',
                                          'Headquarters Location', 'Date added', 'CIK', 'Founded']

    # Additional validations
    assert wiki_data.shape[0] > 0  # Check if there are rows
    assert all(wiki_data['Symbol'].str.isalpha())  # Check if 'Symbol' contains only alphabetic characters
    assert all(wiki_data['Security'].notnull())  # Check if 'Security' does not contain missing values
    assert all(wiki_data['GICS Sector'].notnull())  # Check if 'GICS Sector' does not contain missing values
    assert all(wiki_data['GICS Sub-Industry'].notnull())  # Check if 'GICS Sub-Industry' does not contain missing values


def test_symbol_count(sp):
    data = sp.get_base_data()
    wiki_data = sp.get_data_from_wiki()

    # Check if the number of symbols in the two dataframes match
    assert len(data) == len(wiki_data)

    # Additional validations
    assert len(data['Symbol'].unique()) == len(data)  # Check if 'Symbol' values are unique
    assert len(wiki_data['Symbol'].unique()) == len(wiki_data)  # Check if 'Symbol' values are unique
