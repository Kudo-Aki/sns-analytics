import os, datetime, pandas as pd
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.instagramuser import InstagramUser
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()  # 使わないがローカルテスト用

IG_USER_ID   = os.getenv("IG_USER_ID")
ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
APP_ID       = os.getenv("IG_APP_ID")
APP_SECRET   = os.getenv("IG_APP_SECRET")

# init
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN, api_version="v19.0")
ig_user = InstagramUser(IG_USER_ID)

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
metrics = ig_user.get_insights(
    metric=["impressions","reach","profile_views","website_clicks","follower_count"],
    period="day",
    params={"since": yesterday, "until": yesterday}
)

# 整形
records = [{**m, "date": yesterday} for m in metrics]
df = pd.DataFrame(records)

# BigQuery
bq = bigquery.Client()
table_id = "YOUR_PROJECT_ID.sns.fact_metrics"  # ←プロジェクト ID に直す
bq.load_table_from_dataframe(
    df, table_id,
    job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
).result()

print("✅ ETL 完了")
