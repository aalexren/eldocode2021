#!python

from flask import Flask, json, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import requests

from bs4 import BeautifulSoup

app = Flask(__name__)
# api = Api(app)
CORS(app)
bootstrap = Bootstrap(app)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('children-of-corn-firebase-adminsdk-3hroc-1a3b5f4def.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return "Sorry, try to follow your QR-code"

@app.route('/<string:cart_id>')
def cart(cart_id):
    doc_ref = db.collection(u'carts').document(cart_id)
    doc = doc_ref.get()
    # html_doc = requests.get('https://www.eldorado.ru/cat/detail/ventilyator-napolnyy-status-for-life-st-sf-161m-wt-white/')
    # soup = BeautifulSoup (html_doc.content, 'html.parser')
    # print(soup)
    # print(soup.find('h1', class_='catalogItemDetailHd').text)
    print(doc.get("products"))
    return render_template('index.html', products=doc.get("products"))
    # return jsonify(doc.get("products"))

# class status(Resource):    
#      def get(self):
#          try:
#             doc_ref = db.collection(u'carts').document(u'oBEo885NgJAH7WOceHOA')
#             doc = doc_ref.get()
#             print(doc.get("products"))
#             return {'data': 'Api Running'}
#          except(error): 
#             return {'data': error}

# class Sum(Resource):
#     def get(self, a, b):
#         return jsonify({'data': a+b})

# api.add_resource(status,'/')
# api.add_resource(Sum,'/add/<int:a>,<int:b>')

if __name__ == '__main__':
    app.run(debug=True)