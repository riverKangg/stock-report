import pandas as pd
import FinanceDataReader as fdr

class getSp500List():

    def get_base_data(self):
        sp_data = fdr.StockListing('S&P500').set_index('Symbol')
        return sp_data

    def get_data_from_wiki(self):
        wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        data_from_wiki = pd.read_html(wiki_url, header=0)[0].set_index('Symbol')
        return data_from_wiki
