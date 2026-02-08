import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["JwSW6TpaRHlMdmS9zexWxXdGVlAirGisf4KxC7Bk5ShWFeBGIouGGXkabckGswR5CcSDy/Sa9PzfhJhQFWVDxb74Pmw/fexW8mhW9XG9xiL6ijyQGOnlkhOKb0dZu/Ttx0SWAyBx5GthbuAQLiF71QdB04t89/1O/w1cDnyilFU=
"]
USER_ID = os.environ["U98951ea1ff021258a48030786f0aa1d9
"]

URL = "https://www.daimaru-matsuzakaya.jp/Search.html?keyword=%E4%B8%8B%E9%96%A2+%E6%99%82%E8%A8%88&limit=1&sort=0&page=4"

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}
    data = {"to": USER_ID, "messages":[{"type":"text","text": message}]}
    requests.post(url, headers=headers, json=data)

def check_stock():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    page_text = soup.get_text().replace("\n","").replace(" ","")
    
    if "在庫なし" in page_text:
        send_line_message("❌ 在庫なしです")
        print("在庫なし")
    else:
        send_line_message("✅ 在庫あります！")
        print("在庫あります！")

# GitHub Actions では1回だけ実行
check_stock()

