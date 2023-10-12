import pandas as pd
import FinanceDataReader as fdr


class getSp500List(object):
    def get_data(self):
        # 'Name', 'Sector', 'Industry'
        sp_base = fdr.StockListing('S&P500').set_index('Symbol')
        return sp_base

    def from_wiki(self):
        # 'Security', 'GICS Sector', 'GICS Sub-Industry',
        # 'Headquarters Location', 'Date added', 'CIK', 'Founded'
        sp_wiki = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        sp_wiki_data = pd.read_html(sp_wiki, header=0)[0].set_index('Symbol')
        return sp_wiki_data

