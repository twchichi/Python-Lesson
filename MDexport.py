import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 連接Google試算表
def connect_to_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('每日事件記錄').sheet1
    return sheet

# 添加新事件
def add_event(sheet, people, event, location, item):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_row = [now, people, event, location, item]
    sheet.append_row(new_row)

# 生成markdown文件
def generate_markdown(sheet):
    all_records = sheet.get_all_records()
    markdown = "# 今日事件記錄\n\n"
    for record in all_records:
        if record['時間'].startswith(datetime.now().strftime("%Y-%m-%d")):
            markdown += f"- {record['時間']}: [[{record['人物']}]] {record['事件']} 在 [[{record['地點']}]]\n"
    return markdown

# 發送電子郵件
def send_email(markdown):
    sender_email = "your-email@gmail.com"
    sender_password = "your-password"
    receiver_email = "twchichi@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"每日事件記錄 - {datetime.now().strftime('%Y-%m-%d')}"

    message.attach(MIMEText(markdown, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# 主程序
def main():
    sheet = connect_to_sheet()
    
    # 這裡可以添加一個循環來不斷接收用戶輸入並添加事件
    # 例如:
    while True:
        people = input("請輸入人物 (用逗號分隔多人): ")
        event = input("請輸入事件: ")
        location = input("請輸入地點: ")
        item = input("請輸入物品: ")
        add_event(sheet, people, event, location, item)
        
        if input("是否繼續添加事件? (y/n): ").lower() != 'y':
            break
    
    # 在每天結束時生成markdown並發送郵件
    # 注意: 這裡需要一個定時任務來在每天結束時調用這些函數
    markdown = generate_markdown(sheet)
    send_email(markdown)

if __name__ == "__main__":
    main()

