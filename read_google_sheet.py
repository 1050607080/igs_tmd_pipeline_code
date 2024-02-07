from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 指定您的服务账户密钥 JSON 文件路径
SERVICE_ACCOUNT_FILE = "/Users/tmd/Documents/WebServiceTool/TMD_BuildTool/GoogleApiSecret/ServiceCert.json"

# 指定想要访问的 Google Sheets ID 和范围
# 您可以在 Google Sheets URL 中找到 SHEET_ID
SHEET_ID = '1ICIYmy5YIlE_mMYcVBTGuSsYbUwnsY8VTVuPRAyIJCQ'
RANGE_NAME = '1.66.1!B1:B10'  # 或者您想要读取的特定范围，例如 'Sheet1!A1:E5'

def main():
    # 认证并构建服务
    creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'],
        )

    service = build('sheets', 'v4', credentials=creds)

    # 调用 Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            # 打印列值，根据您的需要修改
            print(row)

if __name__ == '__main__':
    main()