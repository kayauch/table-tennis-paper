import requests
import os

def send_line(message):
    # GitHubのSecretsから値を取得
    line_token = os.environ.get("LINE_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    
    # そもそも変数が読み込めているかチェック
    if not line_token or not user_id:
        print("DEBUG: Error - LINE_ACCESS_TOKEN or LINE_USER_ID is not set in Secrets.")
        return 400

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    
    # LINEの1000文字制限対策
    if len(message) > 1000:
        data["messages"][0]["text"] = message[:990] + "..."

    # 送信実行
    response = requests.post(url, headers=headers, json=data)

    # 【重要】実行ログに送信結果を詳しく出すコード
    print(f"DEBUG: LINE Response Status = {response.status_code}, Response Body = {response.text}")

    return response.status_code
