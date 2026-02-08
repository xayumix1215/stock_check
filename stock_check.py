import time
import requests
from bs4 import BeautifulSoup

# LINE情報
LINE_TOKEN = "JwSW6TpaRHlMdmS9zexWxXdGVlAirGisf4KxC7Bk5ShWFeBGIouGGXkabckGswR5CcSDy/Sa9PzfhJhQFWVDxb74Pmw/fexW8mhW9XG9xiL6ijyQGOnlkhOKb0dZu/Ttx0SWAyBx5GthbuAQLiF71QdB04t89/1O/w1cDnyilFU="
USER_ID = "U98951ea1ff021258a48030786f0aa1d9"

# 在庫確認するページのURL
URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": USER_ID,
        "messages":[{"type":"text","text": message}]
    }
    requests.post(url, headers=headers, json=data)

last_status = None  # 前回の在庫状況

while True:
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    page_text = soup.get_text().replace("\n","").replace(" ","")  # 改行と空白削除

    # 在庫判定（ページに合わせて文字列を変更）
    if "在庫なし" in page_text:
        status = "在庫なし"
    else:
        status = "在庫あり"

    # 状況が変わったときだけ通知
    if status != last_status:
        send_line_message(f"在庫状況が変わりました：{status}")
        print(f"通知送信: {status}")
        last_status = status

    time.sleep(60)  # 60秒ごとにチェック

