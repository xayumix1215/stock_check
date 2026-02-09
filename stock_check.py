import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

STATUS_FILE = "last_status.txt"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages":[{"type":"text","text": message}]
    }
    requests.post(url, headers=headers, json=data)

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    page_text = soup.get_text()

    # 商品名（最初に出てくる h3 を商品名と仮定）
    product_name_tag = soup.find("h3")
    product_name = product_name_tag.get_text(strip=True) if product_name_tag else "商品名不明"

    # 在庫判定
    if "在庫なし" in page_text:
        current_status = "在庫なし"
    else:
        current_status = "在庫あり"

    # 前回の状態を読む
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            last_status = f.read()
    else:
        last_status = ""

    # 状態が変わったら通知
    if current_status != last_status:
        message = (
            "在庫状況が変わりました\n"
            f"商品名：{product_name}\n"
            f"URL：{URL}"
        )
        send_line_message(message)

        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            f.write(current_status)

check_stock()
