import time
import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    data = {"to": USER_ID, "messages":[{"type":"text","text": message}]}
    requests.post(url, headers=headers, json=data)

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    page_text = soup.get_text().replace("\n","").replace(" ","")
    
    if "在庫なし" in page_text:
        send_line_message("❌ 在庫なしです")
        print("在庫なし")
    else:
        print("✅ 在庫あり（通知なし）")

# GitHub Actions では while True は使わず1回だけチェック
check_stock()


