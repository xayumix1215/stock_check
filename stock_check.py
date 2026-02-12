import requests
from bs4 import BeautifulSoup
import os

# ====== 環境変数 ======
LINE_TOKEN = os.environ["LINE_TOKEN"]
USER_ID = os.environ["USER_ID"]

# ====== 在庫確認URL ======
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

# ====== LINE送信関数 ======
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

# ====== 前回の在庫なし数を取得 ======
def get_last_count():
    if os.path.exists("last_count.txt"):
        with open("last_count.txt", "r") as f:
            return int(f.read().strip())
    return None  # 初回

# ====== 今回の在庫なし数を取得 ======
def get_current_count():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    # 「在庫なし」の文字をカウント
    out_of_stock = soup.find_all(string="在庫なし")
    return len(out_of_stock)

# ====== 保存 ======
def save_count(count):
    with open("last_count.txt", "w") as f:
        f.write(str(count))

# ====== メイン処理 ======
last_count = get_last_count()
current_count = get_current_count()

print("==========")
print("前回:", last_count)
print("今回:", current_count)
print("==========")

# 初回は保存だけ
if last_count is None:
    print("初回実行なので保存のみ")
    save_count(current_count)

# 在庫なしが増えたら通知
elif current_count > last_count:
    print("在庫なし増加 → 通知送信")
    send_line(f"在庫なしが増えました\n前回: {last_count}\n今回: {current_count}")
    save_count(current_count)

# 減った場合（在庫復活）
elif current_count < last_count:
    print("在庫なし減少（在庫復活）")
    save_count(current_count)

else:
    print("変化なし")
