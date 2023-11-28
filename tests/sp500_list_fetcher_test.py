import pytest
from stock_report.sp500_list_fetcher import SP500ListFetcher


@pytest.fixture()
def sp():
    return SP500ListFetcher()


def test_get_sp500_data(sp):
    data = sp.get_sp500_data()
    assert data.columns.tolist() == ['Name', 'Sector', 'Industry']

    # Additional validations
    assert data.shape[0] > 0  # Check if there are rows
    assert all(list(filter(lambda x: x.isalpha(), data.index)))  # Check if 'Symbol' contains only alphabetic characters
    assert all(data['Name'].notnull())  # Check if 'Name' does not contain missing values
    assert all(data['Sector'].notnull())  # Check if 'Sector' does not contain missing values
    assert all(data['Industry'].notnull())  # Check if 'Industry' does not contain missing values


def test_get_data_from_wikipedia(sp):
    wiki_data = sp.get_data_from_wikipedia()
    assert wiki_data.columns.tolist() == ['Security', 'GICS Sector', 'GICS Sub-Industry',
                                          'Headquarters Location', 'Date added', 'CIK', 'Founded']

    # Additional validations
    assert wiki_data.shape[0] > 0  # Check if there are rows
    assert all(list(filter(lambda x: x.isalpha(), wiki_data.index)))  # Check if 'Symbol' contains only alphabetic characters
    assert all(wiki_data['Security'].notnull())  # Check if 'Security' does not contain missing values
    assert all(wiki_data['GICS Sector'].notnull())  # Check if 'GICS Sector' does not contain missing values
    assert all(wiki_data['GICS Sub-Industry'].notnull())  # Check if 'GICS Sub-Industry' does not contain missing values


def test_symbol_count(sp):
    data = sp.get_sp500_data()
    wiki_data = sp.get_data_from_wikipedia()

    # Check if the number of symbols in the two dataframes match
    assert len(data) == len(wiki_data)

    # Additional validations
    assert len(data.index.unique()) == len(data)  # Check if 'Symbol' values are unique
    assert len(wiki_data.index.unique()) == len(wiki_data)  # Check if 'Symbol' values are unique
