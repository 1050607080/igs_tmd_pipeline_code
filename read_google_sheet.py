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

    # 認證並構建服務
    creds = Credentials.from_service_account_file(  SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'], )

    service = build('sheets', 'v4', credentials = creds)

    # 調用 Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if values:
        for row in values:
            # 排除特定行
            if row != ['本地路徑', '分支']:
                # 打印列值，根據您的需要修改
                print(row)


if __name__ == '__main__':
    main()