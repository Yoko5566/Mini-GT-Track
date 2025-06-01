from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 初始化瀏覽器
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 無頭模式，若要開啟瀏覽器請註解掉這行
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 開始擷取資料
url = "https://minigt.tsm-models.com/index.php?action=product"
driver.get(url)
time.sleep(5)  # 等待 JavaScript 載入

# 擷取車款資料
models = driver.find_elements(By.CSS_SELECTOR, ".productWrap .productBox")
data = []

for model in models:
    try:
        title = model.find_element(By.CLASS_NAME, "productTitle").text
        number = model.find_element(By.CLASS_NAME, "productNumber").text
        country = model.find_element(By.CLASS_NAME, "productCountry").text
        data.append({
            "名稱": title,
            "型號": number,
            "發行國家": country
        })
    except Exception as e:
        print(f"跳過一筆：{e}")
        continue

driver.quit()

# 儲存為 CSV
df = pd.DataFrame(data)
df.to_csv("data/selenium_catalog.csv", index=False, encoding="utf-8-sig")
print(f"✅ 共擷取 {len(data)} 筆車款資料，已儲存至：data/selenium_catalog.csv")
