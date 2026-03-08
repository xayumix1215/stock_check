import os
import requests

# ==========================
# Secretから取得
# ==========================
LINE_TOKEN = os.getenv("LINE_TOKEN")  # GitHub Secret
GROUP_ID = os.getenv("GROUP_ID")      # GitHub Secret

# ==========================
# LINE通知（手動確認用）
# ==========================
def send_line(message):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": GROUP_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }

    r = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )
    print(f"送信ステータス: {r.status_code}")
    print(f"レスポンス: {r.text}")

# ==========================
# メイン（手動確認用）
# ==========================
def main():
    message = "【テスト通知】このメッセージが届けばOKです"
    send_line(message)

if __name__ == "__main__":
    main()
