import arxiv
import datetime

# 1. 検索条件の設定
search = arxiv.Search(
    query = 'all:"table tennis" OR all:"ping pong"',
    max_results = 10,
    sort_by = arxiv.SortCriterion.SubmittedDate
)

# 2. 論文情報を整形
results_text = f"## 最新の卓球論文リスト (更新日: {datetime.date.today()})\n\n"

for result in search.results():
    results_text += f"- **[{result.title}]({result.entry_id})**\n"
    results_text += f"  - 著者: {', '.join(author.name for author in result.authors)}\n"
    results_text += f"  - 要約: {result.summary[:200]}...\n\n"

# 3. README.md に書き込み
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Table Tennis Paper Aggregator\n\n")
    f.write("筑波大学工学システム学類のプロジェクトとして、最新の卓球論文を自動収集しています。\n\n")
    f.write(results_text)
