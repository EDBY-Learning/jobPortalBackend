from googleapiclient.discovery import build
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DELIMITER = "<:>"
SPREADSHEET_IDS =  {}
FILENAME = "sheet_checkpoint.txt"

with open(str(BASE_DIR)+"/"+FILENAME,'r') as f:
    for line in f:
        if line.strip():
            key, value = line.strip().split(DELIMITER)
            SPREADSHEET_IDS[key] = value

# print(SPREADSHEET_IDS)

def getSheetHandle(creds):
    return build('sheets', 'v4', credentials=creds)

def createSheet(service,name):
    spreadsheet = {
        'properties': {
            'title': name
        }
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    sheetId = spreadsheet.get('spreadsheetId')
    with open(FILENAME,'a') as f:
        f.write(name+DELIMITER+sheetId+"\n")
    return sheetId

def getSheetId(service,name):
    if name in SPREADSHEET_IDS:
        print("Sheet already present")
        return SPREADSHEET_IDS[name]
    else:
        print("New sheet created")
        return createSheet(service,name)
