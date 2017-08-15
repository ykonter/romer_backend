import util

from firebase import firebase
import json

@util.run_once
def fdb():
    f = firebase.FirebaseApplication('https://fam-data.firebaseio.com/', authentication=None)
    return f

def new_entry(data_as_dict, location="/"):
    res = fdb().post(location, data_as_dict)
    print(res)
    return res

fdb()  # init the system
