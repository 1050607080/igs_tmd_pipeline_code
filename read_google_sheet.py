import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 指定您的服務帳戶金鑰 JSON 文件路徑
SERVICE_ACCOUNT_FILE = "/Users/tmd/Documents/WebServiceTool/TMD_BuildTool/GoogleApiSecret/ServiceCert.json"

# 指定想要訪問的 Google Sheets ID 和範圍
# 您可以在 Google Sheets URL 中找到 SHEET_ID
SHEET_ID = '1ICIYmy5YIlE_mMYcVBTGuSsYbUwnsY8VTVuPRAyIJCQ'
RANGE_NAME = '1.66.1!B:C'  # 或者您想要讀取的特定範圍，例如 'Sheet1!A1:E5'

def main():
    # 使用 for 循环遍历 games 列表
    for a in sys.argv:
        print(a)

    print("--------------")
    version = sys.argv[1]
    games_string = sys.argv[2]
    games = games_string.split(" ")

    # 使用 for 循环遍历 games 列表
    for game in games:
        print(game)

    # 認證並構建服務
    creds = Credentials.from_service_account_file(  SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'], )

    service = build('sheets', 'v4', credentials = creds)

    RANGE_NAME = f'{version}!B:C'  # 例如 '1.66.1!B:C'

    # 調用 Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if values:
        for row in values:
            # 排除特定行
            if row[0] in games:
                print(row)


if __name__ == '__main__':
    main()