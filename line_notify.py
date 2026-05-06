import requests
import os

def send_line(message):
    # 環境変数からトークンとIDを取得（後述の.envで設定します）
    line_token = os.environ.get("LINE_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    
    if not line_token or not user_id:
        print("Error: LINE_ACCESS_TOKEN or LINE_USER_ID is not set.")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    
    # メッセージが長すぎるとLINE側でエラーになるため、1000文字で切るなどの対策
    if len(message) > 1000:
        data["messages"][0]["text"] = message[:990] + "..."

    response = requests.post(url, headers=headers, json=data)
    return response.status_code
