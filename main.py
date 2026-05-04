import arxiv
import datetime
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en',target='ja')
# 1. 検索条件の設定
search = arxiv.Search(
    query = 'all:"table tennis" OR all:"ping pong"',
    max_results = 5,
    sort_by = arxiv.SortCriterion.SubmittedDate
)

# 2. 論文情報を整形
results_text = f"## 最新の卓球論文リスト (更新日: {datetime.date.today()})\n\n"

for result in search.results():

    try:
        title_ja = translator.translate(result.title)
        summary_ja = translator.translate(result.summary[:300])
    except Exception:
        title_ja = "翻訳失敗"
        summary_ja = result.summary[:200]
    
    results_text += f"- **{title_ja}**\n"
    results_text += f"- **[{result.title}]({result.entry_id})**\n"
    results_text += f"  - 著者: {', '.join(author.name for author in result.authors)}\n"
    results_text += f"  - 要約: {result.summary[:200]}...\n\n"

# 3. README.md に書き込み
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Table Tennis Paper Aggregator\n\n")
    f.write("研究テーマ決めのため、最新の卓球論文を自動収集しています。\n\n")
    f.write(results_text)
