import pandas as pd
import FinanceDataReader as fdr

class SP500ListFetcher:

    def get_sp500_data(self):
        sp500_data = fdr.StockListing('S&P500').set_index('Symbol')
        sp500_data.index = sp500_data.index.map(self.clean_symbol)
        return sp500_data

    def get_data_from_wikipedia(self):
        wikipedia_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        data_from_wikipedia = pd.read_html(wikipedia_url, header=0)[0].set_index('Symbol')
        return data_from_wikipedia

    def clean_symbol(self, symbol):
        symbol = symbol.replace('BRKB', 'BRK-B').replace('BFB', 'BF-B')
        return symbol
