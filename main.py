from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
from functools import wraps

load_dotenv()

MAIL = os.getenv("MAIL")
MAIL_PASS = os.getenv("MAIL_PASS")
SECURE_KEY = os.getenv("SECURE_KEY")

app = Flask(__name__)
mail_settings = {
    "MAIL_SERVER": 'smtp.yandex.ru',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": MAIL,
    "EMAIL_USER": MAIL,
    "MAIL_PASSWORD": MAIL_PASS

}

app.config.update(mail_settings)
mail = Mail(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['SECUREKEY']
        if not token or token.replace(' ', '') != SECURE_KEY:
            return jsonify({'message': 'invalid token'}), 403
        return f(*args, **kwargs)

    return decorated


@app.route('/email', methods=['POST', 'GET'])
@token_required
def email():
    req = {}
    if request.get_json():
        req = request.get_json()
    city = 'None'
    name = 'None'
    phone = 'None'
    eMail = 'None'
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
    text = name + ' из города ' + city + ' оставил заявку на обратную связь. <br> Номер телефона: ' + phone + '<br> e-mail: ' + eMail
    send_email(subject, MAIL, [MAIL], text, text)

    subject = 'Заявка на обратную связь BattBox'
    text = "Спасибо за ваше обращение! В ближайшее время с вами свяжется наш менеджер, а пока ознакомьтесь с " \
           "презентацией :)"
    send_email(subject, MAIL, [eMail], text, text)
    return jsonify({'status': 'success'}), 200


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = '<p>' + html_body + '</p>'
    with app.app_context():
        mail.send(msg)
