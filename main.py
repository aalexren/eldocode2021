#!python

from flask import Flask, json, jsonify, render_template, redirect, url_for, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import requests

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

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

def send_test_mail(body, receiver_email):
    sender_email = "chernitca@ya.ru"
    # receiver_email = "seva.mikulik@gmail.com"

    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    # filename = "example.txt"
    # msg.attach(MIMEText(open(filename).read()))

    # with open('example.jpg', 'rb') as fp:
    #     img = MIMEImage(fp.read())
    #     img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
    #     msg.attach(img)
        
    # pdf = MIMEApplication(open("example.pdf", 'rb').read())
    # pdf.add_header('Content-Disposition', 'attachment', filename= "example.pdf")
    # msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.yandex.ru', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("chernitca@ya.ru", "xkquqpyqjutyziog")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            print(msg.as_string())
    except Exception as e:
        print(e)

@app.route('/')
def index():
    abort(403)
    return "Sorry, try to follow your QR-code"

@app.route('/<string:cart_id>')
def cart(cart_id):
    print(cart_id)
    try:
        doc_ref = db.collection(u'carts').document(cart_id)
        doc = doc_ref.get()
        products = doc.get("products")
        print(dict(products))
    except Exception as e:
        print(e)
    return render_template('index.html', products=products)

@app.route('/send-email/<string:cart_id>')
def send_email(cart_id):
    # doc_ref = db.collection(u'carts').document(cart_id)
    # doc = doc_ref.get()
    # products = doc.get("products")
    try:
        send_test_mail('''Здравствуйте! 
        Мы сохранили для Вас список товаров в сети магазинов Эльдорадо!
        Чтобы вы ничего не потеряли, мы прикрепили к этому сообщению ссылку: http://children-of-corn-eldorado.herokuapp.com/''' + cart_id,
        u'chernitca@ya.ru')
    except Exception as e:
        print(e)
    return redirect(url_for('cart', cart_id=cart_id))
    # render_template('index.html', products=products)

if __name__ == '__main__':
    # send_test_mail("Привет, Сева Микулик! :D")
    app.run(debug=True)