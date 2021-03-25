from flask import Blueprint, request, jsonify, json
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

from Models import Admin, Data, User
from __init__ import email_service, db

admin = Blueprint('admin', __name__)
admin_auth = HTTPBasicAuth()


@admin_auth.verify_password
def verify_password(username, password):
    """
    Verify the admin password
    :param username:
    :param password:
    :return:
    """
    if username:
        admin = Admin.query.get(username)
        if admin:
            # plaintext compared with chipertext
            return pwd_context.verify(password, admin.password_hash)
    return False


@admin.route('/user_query', methods=['GET'])
@admin_auth.login_required
def query_user():
    """
    Query all username and email
    :return:
    """
    result = User.query.all()

    if result:
        users = []
        for r in result:
            users.append({"username": r.username, "email": r.email})
        return jsonify(users), 200
    else:
        return jsonify({"Info": "No user!"}), 404


@admin.route('/delete_user/<username>', methods=['DELETE'])
@admin_auth.login_required
def delete_user(username):
    """
    Delete the specific user from database

    :param username:
    :return:
    """
    user = User.query.get(username)
    if user is None:
        return jsonify({'Message': "User not found!"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({'Error': repr(e)}), 409

    return jsonify({'Delete': "user {}".format(user.username)}), 200


@admin.route('/query', methods=['GET'])
@admin_auth.login_required
def query():
    """
    Query all data
    :return:
    """
    return Data.query_data()


@admin.route('/query/<date>', methods=['GET'])
@admin_auth.login_required
def query_by_date(date):
    """
    Query data by date
    :param date:
    :return:
    """
    return Data.query_data(date)


@admin.route('/add', methods=['POST'])
@admin_auth.login_required
def add_data():
    """
    Add new data into database
    The default cases and death will be 0
    :return:
    """
    postForm = json.loads(request.get_data(as_text=True))

    if not postForm:
        return jsonify({'Error': 'Empty request body!'}), 400

    data = []
    message = []
    for form in postForm:
        if not 'date' in form:
            return jsonify({'Error': 'Please specify the date!'}), 400
        # Set default value for cases and death
        form.setdefault('cases', 0)
        form.setdefault('death', 0)
        new_data = Data(form['date'], form['cases'], form['death'])
        data.append(new_data)
        message.append(form['date'])

    try:
        db.session.add_all(data)
        db.session.commit()
    except Exception as e:
        return jsonify({'Error': repr(e)}), 409

    return jsonify({'Message': 'Add new item in date {}'.format(message)}), 201


@admin.route('/data/<date>', methods=['PUT', 'DELETE'])
@admin_auth.login_required
def modify_data(date):
    """
    Update the data or delete data
    :param date:
    :return:
    """
    if request.method == 'PUT':
        data = Data.query.get(date)
        if data is None:
            return jsonify({'Message': 'Data not found!'}), 404

        postForm = json.loads(request.get_data(as_text=True))
        if not postForm:
            return jsonify({'Error': 'Empty request body!'}), 400

        data.cases = postForm['cases']
        data.death = postForm['death']
        db.session.commit()

        return jsonify({"Modify": "{}: cases {}, death {}".format(data.date, data.cases, data.death)}), 200
    else:
        data = Data.query.get(date)
        if data is None:
            return jsonify({'Message': "Data not found!"}), 404

        try:
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            return jsonify({'Error': repr(e)}), 409

        return jsonify({'Delete': "{}: cases {}, death {}".format(data.date, data.cases, data.death)}), 200


@admin.route('/get_daily_report', methods=['GET'])
@admin_auth.login_required
def get_daily_report():
    """
    Send an email with a picture that contains a trend of cases and death
    :return:
    """
    admin = Admin.query.get(admin_auth.current_user())
    path = Data.create_picture()
    text = 'Hi {}, this is the latest daily report.'.format(admin.username)

    is_successful, message = email_service.send_image(admin.email, 'Daily report', text, path)
    if is_successful:
        return jsonify({"Info": "Success"}), 200
    else:
        return jsonify({"Error info": str(message)}), 400
