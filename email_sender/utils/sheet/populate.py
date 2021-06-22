def populate_values(service, spreadsheet_id):
    body = {
            'requests': [{
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 10,
                        'startColumnIndex': 0,
                        'endColumnIndex': 10
                    },
                    'cell': {
                        'userEnteredValue': {
                            'stringValue': 'Hello'
                        }
                    },
                    'fields': 'userEnteredValue'
                }
            }]
        }
    service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()