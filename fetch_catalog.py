import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "https://minigt.com/products/"
OUTPUT_FILE = "data/car_catalog.csv"

def get_all_product_links():
    links = []
    page = 1
    while True:
        url = f"{BASE_URL}?page={page}"
        resp = requests.get(url)
        if resp.status_code != 200 or "No products found" in resp.text:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        product_tags = soup.select("a.grid-view-item__link")
        if not product_tags:
            break
        for tag in product_tags:
            link = tag.get("href")
            if link:
                links.append("https://minigt.com" + link)
        page += 1
    return links

def parse_product_detail(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.select_one("h1.product-single__title").get_text(strip=True)
    description = soup.select_one("div.product-single__description")
    desc_text = description.get_text(" ", strip=True) if description else ""
    return {
        "Title": title,
        "URL": url,
        "Description": desc_text
    }

def main():
    os.makedirs("data", exist_ok=True)
    product_links = get_all_product_links()
    data = []
    for url in product_links:
        print(f"Parsing {url}")
        detail = parse_product_detail(url)
        data.append(detail)
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
