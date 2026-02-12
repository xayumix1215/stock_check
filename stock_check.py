import os
import requests
from playwright.sync_api import sync_playwright

# ===== 環境変数 =====
LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

# ===== 在庫確認URL（下関 時計 検索）=====
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88"

# ===== LINE送信 =====
def send_line(message):
    res = requests.post(
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
    print("LINE status:", res.status_code)
    print("LINE response:", res.text)

# ===== 前回数取得 =====
def get_last_count():
    if os.path.exists("last_count.txt"):
        with open("last_count.txt", "r") as f:
            return int(f.read().strip())
    return None

# ===== 保存 =====
def save_count(count):
    with open("last_count.txt", "w") as f:
        f.write(str(count))

# ===== 現在の在庫なし数取得（JS対応）=====
def get_current_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("ページ読み込み開始")
        page.goto(URL, wait_until="networkidle")

        try:
            page.wait_for_selector("text=在庫なし", timeout=15000)
            print("在庫なしテキスト検出")
        except:
            print("在庫なしテキストが見つからない")

        content = page.content()
        browser.close()

    count = content.count("在庫なし")
    print("取得した在庫なし数:", count)
    return count

# ===== メイン =====
print("========== 実行開始 ==========")

last_count = get_last_count()
current_count = get_current_count()

print("前回:", last_count)
print("今回:", current_count)
print("================================")

if last_count is None:
    print("初回実行 → 保存のみ")
    save_count(current_count)

elif current_count > last_count:
    print("在庫なし増加 → 通知送信")
    send_line(f"在庫なし増加\n前回:{last_count}\n今回:{current_count}")
    save_count(current_count)

elif current_count < last_count:
    print("在庫復活 → 通知送信")
    send_line(f"在庫復活しました\n前回:{last_count}\n今回:{current_count}")
    save_count(current_count)

else:
    print("変化なし")
