from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from EmailService import EmailService

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
email_service = EmailService()
