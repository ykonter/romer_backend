from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas

import os

gauth = GoogleAuth()
credential_file = "credentials.cnf"

# save credentials to file (no longer login every run)
gauth.LoadCredentialsFile(credential_file)
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

# save current log-in credentials to file
gauth.SaveCredentialsFile(credential_file)

# create the 'drive' variable
drive = GoogleDrive(gauth)

def retrieve_file_as_xlsx(file_name="Contact Information (Responses)", local_name="fresh_list.xlsx"):
    """look up file on google drive using the built up api-connection
    and saves the file to the root folder as 'local_name'.
    content of xlsx file is returnd as a in-memory dataframe
    """
    # find files
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    f = [f for f in file_list if f['title'] == file_name]  # look for file in file-list
    f = f[0]  # fetch the first hit

    # download file
    my_file = drive.CreateFile({'id' : f['id']})
    my_file.GetContentFile(local_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # return a pandas dataframe
    return pandas.read_excel(local_name)

frame['derived'] = frame['Voornamen'] + " " + frame['Achternaam']

print(frame)
