import requests
import os

def send_line(message):
    # 【修正ポイント】カッコの中は「GitHubで設定した名前（変数名）」を書きます
    line_token = os.environ.get("LINE_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    
    if not line_token or not user_id:
        # これが出ると、GitHubのSecrets設定がうまくいっていません
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
    
    if len(message) > 1000:
        data["messages"][0]["text"] = message[:990] + "..."

    response = requests.post(url, headers=headers, json=data)
    
    # 200以外（401など）が出たら、トークンの値が間違っています
    print(f"LINE Response Status: {response.status_code}")
    return response.status_code
