from flask import Flask, escape, request
import smtplib
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message

load_dotenv()

MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
MAIL_RECEIVER_PASS = os.getenv("MAIL_RECEIVER_PASS")
MAIL_TRANSMITTER = os.getenv("MAIL_TRANSMITTER")
MAIL_TRANSMITTER_PASS = os.getenv("MAIL_TRANSMITTER_PASS")

app = Flask(__name__)
mail_settings = {
    "MAIL_SERVER": 'smtp.yandex.ru',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": MAIL_RECEIVER,
    "EMAIL_USER": MAIL_RECEIVER,
    "MAIL_PASSWORD": MAIL_RECEIVER_PASS

}

app.config.update(mail_settings)
mail = Mail(app)


@app.route('/email',  methods=['POST'])
def email():
    req = request.get_json()
    city = None
    name = None
    phone = None
    eMail = None
    if 'city' in req and 'name' in req and 'phone' in req and 'mail' in req:
        city = req['city']
        name = req['name']
        phone = req['phone']
        eMail = req['mail']
    print(city)
    print(name)
    print(phone)
    print(eMail)
    subject = 'Заявка на обратную связь из города ' + city
    text = name + ' из города ' + city + ' оставил заявку на обратную связь.\nНомер телефона: ' + phone + '\ne-mail: ' + eMail
    send_email(subject, MAIL_RECEIVER, [MAIL_TRANSMITTER], text, '<p>' + text + '</p>')

    # subject = 'Заявка на обратную связь BattBox'
    # text = "С вами свяжется наш менеджер в ближайшее время"
    # send_email(subject, MAIL_TRANSMITTER, [eMail], text, '<p>' + text + '</p>')
    return 'success'


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with app.app_context():
        mail.send(msg)
