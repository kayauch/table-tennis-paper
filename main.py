import arxiv
import datetime
import time  # 1. 時間制御用のライブラリを追加
from deep_translator import GoogleTranslator
from line_notify import send_line 

translator = GoogleTranslator(source='en', target='ja')

def get_translated_papers(query, max_results):
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
    text = ""
    # results() を呼ぶ前に、念のため少し待つ
    time.sleep(3) 
    
    for result in search.results():
        try:
            title_ja = translator.translate(result.title)
            summary_ja = translator.translate(result.summary[:400])
            # 翻訳のループ内でも少し待つ（翻訳サーバーへの配慮）
            time.sleep(1) 
        except Exception:
            title_ja = "（翻訳失敗）"
            summary_ja = result.summary[:200]
        
        text += f"- **{title_ja}**\n"
        text += f"  - 原題: [{result.title}]({result.entry_id})\n"
        text += f"  - 要約: {summary_ja}...\n\n"
    return text



# ...（既存の get_translated_papers 関数などはそのまま）...

# --- 実行部分の最後に追加 ---

# 4. LINE送信用のメッセージを組み立て
line_message = f"🏓 卓球論文アップデート ({datetime.date.today()})\n\n"
line_message += "【注目のAI論文】\n"
# リストからタイトルだけを抽出して短くまとめる工夫をすると読みやすいです
line_message += cv_list.split('\n')[0] # 最初の1件だけ抜粋など

# 5. LINEに送信
status = send_line(line_message)
if status == 200:
    print("LINE notification sent successfully!")
else:
    print(f"Failed to send LINE: {status}")
