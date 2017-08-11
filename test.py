from connect import * # setup the connection with api

# print the files with id's
results = service.files().list(
    pageSize=10,fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))

# fetch a sheets
spreadsheetId = '1ziLI3SUkMDxV9U8F9-sN33iSnAv3ySvvogfYw6xIOfU'
rangeName = 'Sheet1!A1:E'
result = service_sheets.spreadsheets().values().get(
    spreadsheetId=spreadsheetId, range=rangeName).execute()
values = result.get('values', [])
