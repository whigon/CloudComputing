from flask import jsonify
import matplotlib.pyplot as plt
from __init__ import db


class Admin(db.Model):
    """
    Admin model
    """
    __tablename__ = 'admin'
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def __repr__(self):
        return '<Admin %r>' % self.username


class User(db.Model):
    """
    User model
    """
    __tablename__ = 'users'
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password_hash, email):
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Data(db.Model):
    """
    Data model
    """
    __tablename__ = 'data'
    date = db.Column(db.Date, primary_key=True)
    # city = db.Column(db.String(80), nullable=False)
    cases = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=False)

    def __init__(self, date, cases, death):
        self.date = date
        self.cases = cases
        self.death = death

    @staticmethod
    def query_data(date=None):
        """
        Query data from database
        If date is none, return all data, else return the specific date
        :param date:
        :return:
        """
        if date:
            result = Data.query.get(date)
            if result is None:
                return jsonify({"Error": "No data in given date!"}), 404

            data = {
                'date': result.date,
                'cases': result.cases,
                'death': result.death
            }

            return jsonify(data), 200
        else:
            result = Data.query.all()
            data = []

            for r in result:
                new_record = {
                    'date': r.date,
                    'cases': r.cases,
                    'death': r.death
                }
                data.append(new_record)

            if len(data) == 0:
                return jsonify({"Error": "Data not found"}), 404
            else:
                return jsonify(data), 200

    @staticmethod
    def create_picture():
        """
        Create the picture to show the trend of cases and death
        :return:
        """
        result = Data.query.all()

        date = []
        cases = []
        death = []
        for r in result:
            date.append(str(r.date))
            cases.append(r.cases)
            death.append(r.death)

        pic_path = 'daily_report_{}.png'.format(date[-1])

        # fig = plt.figure(figsize=(10, 8))
        plt.xticks(rotation=90)
        l1 = plt.plot(date, cases, 'ro-', label='cases')
        l2 = plt.plot(date, death, 'g+-', label='death')

        plt.plot(date, cases, 'ro-')
        plt.plot(date, death, 'g+-')
        plt.title('Covid-19 daily report')
        plt.xlabel('date')
        plt.legend()
        plt.savefig(pic_path)
        return pic_path

    def __repr__(self):
        return '<Data %d>' % self.date
