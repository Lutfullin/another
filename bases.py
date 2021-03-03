
'''
import sqlite3
#from sqlite3 import Error


conn = sqlite3.connect(r"D:\sqlbases\base.db")
c = conn.cursor()

try:
    c.execute("CREATE TABLE reestr(i INTEGER PRIMARY KEY, name STRING, protein real, fat real, carboh real, calories real)")
except Exception:
    pass

c.execute("INSERT INTO reestr VALUES(1,'пепси', 1, 2, 3, 23)")

conn.commit()



conn.close()
'''



# cred_obj = firebase_admin.credentials.Certificate('D:\sqlbases\fatcalculator-ee746-firebase-adminsdk-2wjzv-a5ef5a5653.json')
# default_app = firebase_admin.initialize_app(cred_object, {
# 	'databaseURL':databaseURL
# 	})

'''
import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate(r"D:\sqlbases\fatcalculator-ee746-firebase-adminsdk-2wjzv-a5ef5a5653.json")
firebase_admin.initialize_app(cred)

firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)


new_user = 'Ozgur Vatansever'

result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print (result)
'''

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate(r"D:\sqlbases\fatcalculator-ee746-firebase-adminsdk-2wjzv-a5ef5a5653.json")

'''
firebase_admin.initialize_app(cred)
'''
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fatcalculator-ee746-default-rtdb.firebaseio.com/'
})



ref = db.reference('restricted_access/secret_document')
print(ref.get())


users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})


users_ref = ref.child('ass')
data = {
        "Book1":
        {
            "Title": "The Fellowship of the Ring",
            "Author": "J.R.R. Tolkien",
            "Genre": "Epic fantasy",
            "Price": 100
        },
        "Book2":
        {
            "Title": "The Two Towers",
            "Author": "J.R.R. Tolkien",
            "Genre": "Epic fantasy",
            "Price": 100	
        },
        "Book3":
        {
            "Title": "The Return of the King",
            "Author": "J.R.R. Tolkien",
            "Genre": "Epic fantasy",
            "Price": 100
        },
        "Book4":
        {
            "Title": "Brida",
            "Author": "Paulo Coelho",
            "Genre": "Fiction",
            "Price": 100
        }
}

users_ref.set(data)

users_ref = ref.child('one')
data =  [66.25, 333, 333, 1, 1234.5]

users_ref.set(data)

