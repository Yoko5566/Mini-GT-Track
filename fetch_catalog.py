import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

# 建立資料夾
os.makedirs("data", exist_ok=True)

# 設定 URL
url = "https://minigt.tsm-models.com/index.php?action=product"

# 發送 GET 請求
response = requests.get(url)
response.encoding = 'utf-8'

# 確保請求成功
if response.status_code != 200:
    raise Exception(f"❌ 網站回應失敗，HTTP 狀態碼：{response.status_code}")

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 抓取所有產品項目
products = soup.select("div.product-listing div.product")

catalog = []

for p in products:
    try:
        title = p.select_one("div.product-name").get_text(strip=True)
        code = p.select_one("div.product-code").get_text(strip=True).replace("Item No: ", "")
        image_url = p.select_one("img")["src"]
        catalog.append({
            "Model Name": title,
            "Product Code": code,
            "Image URL": image_url,
            "Source": "Mini GT Official"
        })
    except Exception as e:
        print("⚠️ 解析單一產品時出錯：", e)

# 轉成 DataFrame 並儲存成 CSV
df = pd.DataFrame(catalog)
csv_path = "data/car_catalog.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"✅ 共擷取 {len(df)} 筆車款資料，已儲存至：{csv_path}")
