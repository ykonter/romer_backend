from pydrive.auth import GoogleAuth
import os
gauth = GoogleAuth()
# gauth.LocalWebserverAuth()

# save to file
gauth.LoadCredentialsFile("credentials.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("credentials.txt")


from pydrive.drive import GoogleDrive
drive = GoogleDrive(gauth)


# my own part
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#print(file_list)
file_name = "Contact Information (Responses)"
[print('title:: {}, id: {}'.format(file['title'], file['id'])) for file in file_list]
f = [f for f in file_list if f['title'] == file_name]
f = f[0] # only first hit
# print(f) # found the file
# m_t = {'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
# print(f.FetchMetadata(fields='mimeType'))
my_file = drive.CreateFile({'id' : f['id']})
my_file.GetContentFile("fresh_list.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#@file = drive.CreateFile({'id': "1ziLI3SUkMDxV9U8F9-sN33iSnAv3ySvvogfYw6xIOfU"})
#content = file.GetContentString()
#print(content)

import pandas
frame = pandas.read_excel('fresh_list.xlsx')
frame['derived'] = frame['Voornamen'] + " " + frame['Achternaam']

print(frame)
