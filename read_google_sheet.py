import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 指定您的服務帳戶金鑰 JSON 文件路徑
SERVICE_ACCOUNT_FILE = "/Users/tmd/Documents/WebServiceTool/TMD_BuildTool/GoogleApiSecret/ServiceCert.json"

# 指定想要訪問的 Google Sheets ID 和範圍
# 您可以在 Google Sheets URL 中找到 SHEET_ID
SHEET_ID = '1ICIYmy5YIlE_mMYcVBTGuSsYbUwnsY8VTVuPRAyIJCQ'
RANGE_NAME = '1.66.1!B1:B10'  # 或者您想要讀取的特定範圍，例如 'Sheet1!A1:E5'

def main():
    param1 = sys.argv[1]
    print("param1",param1)
    # 認證並構建服務
    creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'],
        )

    service = build('sheets', 'v4', credentials = creds)

    # 調用 Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('沒有找到數據。')
    else:
        for row in values:
            # 打印列值，根據您的需要修改
            print(row)

if __name__ == '__main__':
    main()