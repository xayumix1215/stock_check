import os
import requests
from playwright.sync_api import sync_playwright

LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

def send_line(message):
    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "to": USER_ID,
            "messages": [{"type": "text", "text": message}]
        }
    )

def get_last_count():
    if os.path.exists("last_count.txt"):
        with open("last_count.txt") as f:
            return int(f.read().strip())
    return None

def save_count(count):
    with open("last_count.txt", "w") as f:
        f.write(str(count))

def get_current_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(8000)

        count = page.locator("text=在庫なし").count()

        browser.close()

    return count

print("===== 実行開始 =====")

last_count = get_last_count()
current_count = get_current_count()

print("前回:", last_count)
print("今回:", current_count)

if last_count is None:
    save_count(current_count)

elif current_count > last_count:
    message = f"""【在庫チェック】
在庫なし表示数：{current_count}

{URL}
"""
    send_line(message)
    save_count(current_count)

elif current_count < last_count:
    save_count(current_count)

else:
    print("変化なし")
