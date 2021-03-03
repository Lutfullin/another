
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"D:\sqlbases\fatcalculator-ee746-firebase-adminsdk-2wjzv-a5ef5a5653.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fatcalculator-ee746-default-rtdb.firebaseio.com/'
})

ref = db.reference('Fat_Calculator')

products = ref.child('Comon_products')




data = {
        "яблоко":
        {
            "protein": 0.4,
            "fat": 0.4,
            "cabroh": 9.8,
            "callories": 100
        },
        "груша":
        {
            "protein": 0.4,
            "fat": 0.4,
            "cabroh": 9.8,
            "callories": 100	
        }
}

products.set(data)
