from flask import jsonify
import matplotlib.pyplot as plt
from matplotlib import ticker

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
        If date is none, return all data, else return data in the specific date
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
                return jsonify({"Error": "Data not found!"}), 404
            else:
                return jsonify(data), 200

    @staticmethod
    def create_picture():
        """
        Create the picture to show the trend of cases and death
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

        fig = plt.figure(figsize=(100, 50))

        ax1 = fig.add_subplot(111)
        ax1.set_title("Covid-19 Daily Report", fontsize=70)
        ax1.set_ylabel('Cases', fontsize=40)

        plt.xticks(rotation=270, fontsize=40)
        plt.yticks(fontsize=50)
        plot1 = ax1.plot(date, cases, '-*', color='r', label='cases')

        ax2 = ax1.twinx()  # this is the important function

        plot2 = ax2.plot(date, death, '-o', color='g', label='death')
        lines = plot1 + plot2

        ax2.set_ylabel('Death', fontsize=40)
        ax2.set_xlabel('Date', fontsize=70)
        ax2.tick_params(axis='y', labelsize=50)

        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(12))
        ax1.legend(lines, [l.get_label() for l in lines], fontsize=50)

        plt.savefig(pic_path)
        plt.cla()
        plt.clf()
        plt.close()
        return pic_path

    def __repr__(self):
        return '<Data %d>' % self.date
