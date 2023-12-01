import os
from glob import glob
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from datetime import datetime

from utils import *

report_path = '/Users/samsung/PycharmProjects/stock-report/output/sp500_report/'
os.makedirs(report_path, exist_ok=True)

content = "# Key Financial Metrics Analysis for S&P 500 Companies \n\n"
formatted_date = get_formmated_date()
content += f"- Report Date: {formatted_date}\n"

# 가장 최근 지표 데이터 불러오기
root_dir = get_root_directory()
sp500_folder = max(glob(f"{root_dir}/output/sp500_20*"))
data_reference_date = sp500_folder.split('sp500_')[-1].replace('.csv', '')
content += f"- Data Reference Date: {data_reference_date}\n\n"

# Market Cap
content += '--- \n'
content += f"## MarketCap top 10\n\n"
marketcap = pd.read_csv(f'{sp500_folder}/top_MarketCap.csv', sep='\t')
content += tabulate(marketcap, headers='keys', tablefmt='github') + "\n\n"

# PBR
content += '--- \n'
content += f"## PBR Analysis\n\n"
grp_pbr = pd.read_csv(f'{sp500_folder}/GRP_PBR.csv', sep='\t')
content += tabulate(grp_pbr, headers='keys', tablefmt='github') + "\n\n"

content += '--- \n'
content += f"## PBR Top 10 by sector\n\n"
pbr = pd.read_csv(f'{sp500_folder}/top_PBR_Sector.csv', sep='\t')

for sector in set(pbr.Sector):
    content += f"#### {sector} Sector - PBR Analysis\n\n"
    data = pbr[pbr.Sector == sector]
    content += tabulate(data, headers='keys', tablefmt='github') + "\n\n"

# PER
content += '--- \n'
content += f"## Sector - PER Analysis\n\n"
grp_per = pd.read_csv(f'{sp500_folder}/GRP_PER.csv', sep='\t')
content += tabulate(grp_per, headers='keys', tablefmt='github') + "\n\n"

content += '--- \n'
content += f"## PER Top 10 by sector\n\n"
per = pd.read_csv(f'{sp500_folder}/top_PER_Sector.csv', sep='\t')

for sector in set(per.Sector):
    content += f"#### {sector} Sector - PBR Analysis\n\n"
    data = per[per.Sector == sector]
    content += tabulate(data, headers='keys', tablefmt='github') + "\n\n"

# Markdown 작성
with open(f'{report_path}/S&P500_report_{formatted_date}.md', "w") as f:
    f.write(content)