import os, base64, pathlib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

# 添付：txt を PDF に変換せずそのまま送る場合は path を変えてください
file_path = pathlib.Path("weekly_report.txt")
with open(file_path,"rb") as f:
    data = base64.b64encode(f.read()).decode()

attachment = Attachment(
    FileContent(data),
    FileName(file_path.name),
    FileType("text/plain"),
    Disposition("attachment")
)

message = Mail(
    from_email="no-reply@sakatsura.or.jp",
    to_emails=os.getenv("SEND_TO"),
    subject="【酒列磯前神社】週次SNSレポート",
    html_content="自動生成されたレポートを添付いたします。"
)
message.attachment = attachment
sg.send(message)
print("✅ メール送信完了")
