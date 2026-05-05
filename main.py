import arxiv
import datetime
import time  # 1. 時間制御用のライブラリを追加
from deep_translator import GoogleTranslator
from plyer import notification

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

# --- 実行部分 ---

# 1. 汎用的な最新論文
general_query = 'all:"table tennis" OR all:"ping pong"'
general_list = get_translated_papers(general_query, 5)

# 2. 次の検索の前に「5秒」休憩を入れる（これが重要！）
print("Waiting for next request...")
time.sleep(5)

# 3. 画像処理に特化した論文
cv_query = '(all:"table tennis" OR all:"ping pong") AND (all:"image processing" OR all:"computer vision" OR all:"deep learning")'
cv_list = get_translated_papers(cv_query, 5)

# --- 以下、README書き出し処理 ---
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Table Tennis Paper Aggregator\n\n")
    f.write(f"最終更新日: {datetime.date.today()}\n\n")
    f.write("## 📷 画像処理・AI活用 厳選5選\n\n")
    f.write(cv_list)
    f.write("---\n\n")
    f.write("## 🏓 最新の卓球論文全般\n\n")
    f.write(general_list)

notification.notify(
    title='最新の卓球論文',
    message='画像処理に関する新しい論文が3件見つかりました。',
    app_name='Table Tennis Bot',
    timeout=10 # 10秒間表示
)
