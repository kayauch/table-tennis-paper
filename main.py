import arxiv
import datetime
import time
from deep_translator import GoogleTranslator
from line_notify import send_line  # 自作ファイルのインポート

translator = GoogleTranslator(source='en', target='ja')

def get_translated_papers(query, max_results):
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
    text = ""
    time.sleep(3) 
    
    for result in search.results():
        try:
            title_ja = translator.translate(result.title)
            summary_ja = translator.translate(result.summary[:400])
            time.sleep(1) 
        except Exception:
            title_ja = "（翻訳失敗）"
            summary_ja = result.summary[:200]
        
        text += f"- **{title_ja}**\n"
        text += f"  - 原題: [{result.title}]({result.entry_id})\n"
        text += f"  - 要約: {summary_ja}...\n\n"
    return text

# --- 実行部分 ---

# 1. 汎用的な最新論文の取得
general_query = 'all:"table tennis" OR all:"ping pong"'
general_list = get_translated_papers(general_query, 3)

print("Waiting for next request...")
time.sleep(5)

# 2. 画像処理に特化した論文の取得 (ここで cv_list を定義)
cv_query = '(all:"table tennis" OR all:"ping pong") AND (all:"image processing" OR all:"computer vision" OR all:"deep learning")'
cv_list = get_translated_papers(cv_query, 3)

# 3. LINE送信用のメッセージ組み立て (定義した後に使う)
line_message = f"🏓 卓球論文アップデート ({datetime.date.today()})\n\n"
if cv_list.strip():
    # 最初の論文タイトルだけを抽出して通知
    first_paper = cv_list.split('\n')[0].replace("- **", "").replace("**", "")
    line_message += f"【注目】{first_paper}\n\n詳細はGitHubのREADME(https://github.com/kayauch/table-tennis-paper/blob/main/README.md)を確認してください。"
else:
    line_message += "本日、画像処理系の新着論文はありませんでした。"

# 4. LINE送信の実行
send_line(line_message)

# --- README書き出し ---
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Table Tennis Paper Aggregator\n\n")
    f.write(f"最終更新日: {datetime.date.today()}\n\n")
    f.write("## 📷 画像処理・AI活用 厳選論文\n\n")
    f.write(cv_list if cv_list.strip() else "該当なし\n")
    f.write("---\n\n")
    f.write("## 🏓 最新の卓球論文全般\n\n")
    f.write(general_list if general_list.strip() else "該当なし\n")
