#!python

from flask import Flask, json, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# cred = credentials.Certificate('children-of-corn-firebase-adminsdk-3hroc-1a3b5f4def.json')
# firebase_admin.initialize_app(cred)


# db = firestore.client()
# doc_ref = db.collection(u'carts').document(u'oBEo885NgJAH7WOceHOA')
# doc = doc_ref.get().to_dict()
# print(doc)


class status(Resource):    
     def get(self):
         try:
            return {'data': 'Api running'}
         except(error): 
            return {'data': error}

class Sum(Resource):
    def get(self, a, b):
        return jsonify({'data': a+b})

api.add_resource(status,'/')
api.add_resource(Sum,'/add/<int:a>,<int:b>')

if __name__ == '__main__':
    app.run(debug=True)