import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def fetch_news():
    url = "https://minigt.tsm-models.com/index.php?action=news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_titles = soup.select('div.news_title > a')
    news_dates = soup.select('div.news_date')

    rows = [["新聞標題", "連結", "發布日期"]]
    for title, date in zip(news_titles, news_dates):
        link = "https://minigt.tsm-models.com/" + title.get('href')
        rows.append([title.text.strip(), link, date.text.strip()])

    # 正確產出 .csv
    filename = f"news_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    fetch_news()
