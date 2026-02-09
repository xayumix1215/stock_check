import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

def send_line_message(message):
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "to": USER_ID,
            "messages": [{"type": "text", "text": message}]
        }
        res = requests.post(url, headers=headers, json=data, timeout=10)
        print("LINE送信ステータス:", res.status_code)
    except Exception as e:
        print("LINE送信エラー:", e)

def load_last_status():
    try:
        with open("last_status.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_status(status):
    with open("last_status.txt", "w") as f:
        f.write(status)

def check_stock():
    try:
        res = requests.get(URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        page_text = soup.get_text().replace("\n", "").replace(" ", "")

        if "在庫なし" in page_text:
            current_status = "在庫なし"
        else:
            current_status = "在庫あり"

        last_status = load_last_status()

        if current_status != last_status:
            send_line_message("在庫状況が変わりました")
            save_last_status(current_status)
            print("状態変化あり → 通知送信")
        else:
            print("状態変化なし")

    except Exception as e:
        print("在庫チェックエラー:", e)

# 1回だけ実行
check_stock()
