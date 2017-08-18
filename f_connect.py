import util

from firebase import firebase
import json

# the prebase way
import pyrebase

@util.run_once
def fdb():
    config = {
      "apiKey": "AIzaSyAgaU3OQHbglNDTmPrQlYr0hQg_M_MyA5Y",
      "authDomain": "fam-data.firebaseapp.com",
      "databaseURL": "https://fam-data.firebaseio.com",
      "storageBucket": "fam-data.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def new_entry(data_as_dict, location="/"):
    res = fdb().child(location).push(data_as_dict)
    return res

def set(key, data_as_dict, location="/"):
    if key != []:
        res = fdb().child(location).child(key).set(data_as_dict)
        return res

def get_all(location="/"):
    return fdb().get(location, None)

if __name__ == '__main__':
    people = fdb().child("people").get()  # fetch all people
    p2 = fdb().child("/people").order_by_child("Achternaam").equal_to("Konter").get() # fetch subset data
    for peep in p2.each():
        print(peep.key())
        print(peep.val())
