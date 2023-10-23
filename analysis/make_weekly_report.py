import os
from datetime import datetime

# 1. CHART LINK - 캡쳐 필요
world_map_link = 'https://finviz.com/map.ashx?t=geo&st=w1'
sp500_sector_link = 'https://finviz.com/groups.ashx'
sp500_map_link = 'https://finviz.com/map.ashx?st=w1'
content1 = (f"글로벌 증시\n{world_map_link}\n"
            f"섹터별 현황\n{sp500_sector_link}\n{sp500_map_link}")

# 2.

# Markdown 작성
dt = datetime.now().strftime('%y%m%d')
title = f"### Weekly Report {dt}"
markdown_content = f"# {title}\n\n{content1}"

# Markdown 파일을 output 폴더에 저장
output_folder = "output"
os.makedirs(f'{output_folder}', exist_ok=True)
output_file = f"{output_folder}/{title.replace(' ', '_').lower()}.md"

with open(output_file, "w") as file:
    file.write(markdown_content)

print(f"Markdown 파일이 {output_file}에 생성되었습니다.")