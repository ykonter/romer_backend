import util

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas
from httplib2 import socks
import httplib2

import os
import sys

@util.run_once  # enforce 1 connection
def drive():
    gauth = GoogleAuth()
    credential_file = "credentials.cnf"

    # check for proxy settings
    proxy_val = os.environ.get('HTTPS_PROXY')
    if proxy_val:
        proxy_string = proxy_val.split(':')
        port = int(proxy_string[-1])
        server = proxy_string[1].replace('/','')
        myprox = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP_NO_TUNNEL, server, port)  # not PROXY_TYPE_SOCKS5
        httpProxy = httplib2.Http(proxy_info=myprox)
        gauth.http = httpProxy
    try:
        # save credentials to file (no longer login every run)
        gauth.LoadCredentialsFile(credential_file)
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
    except:
        print('always keep failing')
        print(sys.exc_info())

    # save current log-in credentials to file
    gauth.SaveCredentialsFile(credential_file)

    # create the 'drive' variable
    drive = GoogleDrive(gauth)
    return drive


def retrieve_file_as_xlsx(file_name="Contact Information (Responses)", local_name="fresh_list.xlsx"):
    """look up file on google drive using the built up api-connection
    and saves the file to the root folder as 'local_name'.
    content of xlsx file is returnd as a in-memory dataframe
    """
    # find files
    file_list = drive().ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    f = [f for f in file_list if f['title'] == file_name]  # look for file in file-list
    f = f[0]  # fetch the first hit

    # download file
    my_file = drive().CreateFile({'id' : f['id']})
    my_file.GetContentFile(local_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # return a pandas dataframe
    return pandas.read_excel(local_name)

## load the module correctly
drive()
retrieve_file_as_xlsx()
