import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://minigt.fandom.com/wiki/Full_Collection"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格
tables = soup.find_all('table')

# 假設第一個表格是我們需要的
table = tables[0]

# 解析表格
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cols = row.find_all('td')
    if len(cols) >= 5:
        code = cols[0].text.strip()
        name = cols[1].text.strip()
        lhd_rhd = cols[2].text.strip()
        brand = cols[3].text.strip()
        year = cols[4].text.strip()
        data.append([code, name, lhd_rhd, brand, year])

# 建立 DataFrame
df = pd.DataFrame(data, columns=['Code', 'Name', 'LHD/RHD', 'Brand', 'Year'])

# 儲存為 CSV
df.to_csv('data/mini_gt_wiki_data.csv', index=False)

print(f"✅ 共擷取 {len(df)} 筆車款資料，已儲存至 data/mini_gt_wiki_data.csv")
