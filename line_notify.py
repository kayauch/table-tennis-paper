import requests
import os

def send_line(message):
  from line_notify import send_line  # 自作したファイルを読み込む

def main():
    # 1. 論文を集める処理
    papers = collect_papers() 
    
    # 2. メッセージを組み立てる
    msg = f"今日の論文はこれです：\n{papers}"
    
    # 3. LINEに送る
    send_line(msg)

if __name__ == "__main__":
    main()
    pass
