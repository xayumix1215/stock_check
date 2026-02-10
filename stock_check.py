import requests
from bs4 import BeautifulSoup
import os
import subprocess

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]
EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "")

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
    if not os.path.exists(STATUS_FILE):
        return None
    with open(STATUS_FILE, "r") as f:
        return int(f.read().strip())

def save_and_commit_count(count):
    with open(STATUS_FILE, "w") as f:
        f.write(str(count))

    subprocess.run(["git", "config", "user.name", "github-actions"])
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"])
    subprocess.run(["git", "add", STATUS_FILE])
    subprocess.run(["git", "commit", "-m", "update count"], check=False)
    subprocess.run(["git", "push"], check=False)

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    count = text.count("在庫なし")
    last_count = get_last_count()

    # 手動は必ず通知
    if EVENT_NAME == "workflow_dispatch":
        send_line_message("【手動確認】在庫チェックしました\n" + URL)

    # 「在庫なし」という文字が増えたら通知
    elif last_count is not None and count > last_count:
        send_line_message("在庫状況が変わりました\n" + URL)

    save_and_commit_count(count)

check_stock()
