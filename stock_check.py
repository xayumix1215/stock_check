from playwright.sync_api import sync_playwright
import os
import requests

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"
COUNT_FILE = "last_count.txt"

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

def send_line(msg):
    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "to": USER_ID,
            "messages": [{"type": "text", "text": msg}],
        },
    )

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")
    current_count = text.count("在庫なし")

    browser.close()

try:
    with open(COUNT_FILE, "r") as f:
        last_count = int(f.read())
except:
    last_count = 0

if current_count > last_count:
    send_line(f"📢 在庫なしが増えた！\n{last_count} → {current_count}")

with open(COUNT_FILE, "w") as f:
    f.write(str(current_count))
