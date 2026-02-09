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

def get_last_count():
    try:
        with open(STATUS_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return None

def save_count(count):
    with open(STATUS_FILE, "w") as f:
        f.write(str(count))

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    page_text = soup.get_text()
    count = page_text.count("在庫なし")

    last_count = get_last_count()

    # 初回実行時は保存だけして通知しない
    if last_count is None:
        save_count(count)
        return

    # 数が変わったときだけ通知
    if count != last_count:
        message = (
            "在庫状況が変わりました\n"
            f"URL：{URL}"
        )
        send_line_message(message)

    save_count(count)

check_stock()

send_line_message("手動テスト通知\n" + URL)
