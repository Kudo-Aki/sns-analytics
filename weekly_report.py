import os, pandas as pd
from datetime import date, timedelta
from google.cloud import bigquery
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
bq = bigquery.Client()

last_mon = (date.today() - timedelta(days=date.today().weekday()+7)).isoformat()
last_sun = (date.today() - timedelta(days=date.today().weekday()+1)).isoformat()

sql = f"""
SELECT caption, reach, likes, comments, saves,
       ROUND(100*(likes+comments+saves)/NULLIF(reach,0),2) AS er
FROM `YOUR_PROJECT_ID.sns.fact_metrics`
WHERE date BETWEEN '{last_mon}' AND '{last_sun}'
ORDER BY er DESC
LIMIT 5
"""
df = bq.query(sql).to_dataframe()

prompt = f"""
あなたは神社公式InstagramのSNSコンサルタント。
先週({last_mon}〜{last_sun})の上位投稿と数値はこちら。
{df.to_markdown(index=False)}

1) 次週注力すべきテーマを 3 つ
2) 最適な投稿フォーマット(画像 / リール / ストーリーズ)
3) 推奨投稿曜日・時間帯
4) 添える日本語ハッシュタグ 5 個

箇条書きで提案してください。
"""
resp = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt}],
    temperature=0.7
)

with open("weekly_report.txt","w",encoding="utf-8") as f:
    f.write(resp.choices[0].message.content)

print("✅ レポート生成完了")
