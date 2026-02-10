import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"
STATUS_FILE = "last_count.txt"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=data)

def load_last_count():
    try:
        with open(STATUS_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_count(count):
    with open(STATUS_FILE, "w") as f:
        f.write(str(count))

def check_stock():
    res = requests.get(URL, timeout=20)
    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text()
    current_count = text.count("在庫なし")
    last_count = load_last_count()

    # 🔔 手動実行は必ず通知
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        send_line_message(
            "【手動確認】\n"
            "在庫ページを確認しました。\n"
            f"{URL}"
        )
        save_count(current_count)
        return

    # 🔔 在庫なしが増えたら通知
    if current_count > last_count:
        send_line_message(
            "在庫状況が変わりました\n"
            f"{URL}"
        )

    save_count(current_count)

check_stock()
