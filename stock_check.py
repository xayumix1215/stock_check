import os
import requests
from playwright.sync_api import sync_playwright

# ==========================
# 設定
# ==========================
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"
LAST_COUNT_FILE = "last_count.txt"

LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("USER_ID")


# ==========================
# 在庫なし数を取得
# ==========================
def get_out_of_stock_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)

        content = page.content()
        browser.close()

    # 「在庫なし」の文字数をカウント
    return content.count("在庫なし")


# ==========================
# 前回値読み込み
# ==========================
def load_last_count():
    if not os.path.exists(LAST_COUNT_FILE):
        return 0
    with open(LAST_COUNT_FILE, "r") as f:
        return int(f.read().strip())


# ==========================
# 前回値保存
# ==========================
def save_last_count(count):
    with open(LAST_COUNT_FILE, "w") as f:
        f.write(str(count))


# ==========================
# LINE通知
# ==========================
def send_line(message):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )


# ==========================
# メイン処理
# ==========================
def main():
    print("===== 実行開始 =====")

    current_count = get_out_of_stock_count()
    last_count = load_last_count()

    print(f"前回: {last_count}")
    print(f"今回: {current_count}")

    # 🔥 増えた時だけ通知
    if current_count > last_count:
        message = (
            "【在庫変動通知】\n"
            "在庫なしの商品が増えました。\n\n"
            f"{URL}"
        )
        send_line(message)
        print("通知送信しました")

    else:
        print("変化なし（通知なし）")

    # 常に最新値を保存
    save_last_count(current_count)


if __name__ == "__main__":
    main()
