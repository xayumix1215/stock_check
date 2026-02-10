import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"
STATUS_FILE = "last_count.txt"

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

def send_line(message):
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

# 🔹 手動実行かどうか判定
IS_MANUAL = os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(3000)

    content = page.content()
    browser.close()

# 「在庫なし」という文字数をカウント
current_count = content.count("在庫なし")

# 前回の数を読む
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        last_count = int(f.read().strip())
else:
    last_count = 0

# 🔔 通知ロジック
if IS_MANUAL:
    send_line(
        f"【手動実行】\n在庫なし表示数：{current_count}\n\n{URL}"
    )
elif current_count > last_count:
    send_line(
        f"【変化あり】在庫なしが増えました\n{last_count} → {current_count}\n\n{URL}"
    )

# 今回の数を保存
with open(STATUS_FILE, "w") as f:
    f.write(str(current_count))
