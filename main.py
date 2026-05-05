import arxiv
import datetime
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='ja')

def get_translated_papers(query, max_results):
    """論文を検索して翻訳済みのテキストを返す関数"""
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
    text = ""
    for result in search.results():
        try:
            title_ja = translator.translate(result.title)
            summary_ja = translator.translate(result.summary[:400])
        except Exception:
            title_ja = "（翻訳失敗）"
            summary_ja = result.summary[:200]
        
        text += f"- **{title_ja}**\n"
        text += f"  - 原題: [{result.title}]({result.entry_id})\n"
        text += f"  - 要約: {summary_ja}...\n\n"
    return text

# 1. 汎用的な最新論文（5件）
general_query = 'all:"table tennis" OR all:"ping pong"'
general_list = get_translated_papers(general_query, 5)

# 2. 画像処理に特化した論文（5件）
# 「卓球」かつ「画像処理・コンピュータビジョン」に関連するもの
cv_query = '(all:"table tennis" OR all:"ping pong") AND (all:"image processing" OR all:"computer vision" OR all:"deep learning")'
cv_list = get_translated_papers(cv_query, 5)

# 3. README.md に書き込み
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Table Tennis Paper Aggregator\n\n")
    f.write(f"最終更新日: {datetime.date.today()}\n\n")
    
    f.write("## 📷 画像処理・AI活用 厳選5選\n")
    f.write("画像解析、動作認識、ディープラーニングなどを用いた研究です。\n\n")
    f.write(cv_list)
    
    f.write("---\n\n") # 区切り線
    
    f.write("## 🏓 最新の卓球論文全般\n")
    f.write("分野を問わず、新しく投稿された論文です。\n\n")
    f.write(general_list)
