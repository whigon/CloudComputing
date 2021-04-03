from flask import Blueprint, jsonify, json, request
from Models import User, Data
from passlib.apps import custom_app_context as pwd_context
from __init__ import email_service, db
from flask_httpauth import HTTPBasicAuth

user = Blueprint('user', __name__)
user_auth = HTTPBasicAuth()


@user.route('/new_user', methods=["POST"])
def new_user():
    """
    Create a new user account
    """
    postForm = json.loads(request.get_data(as_text=True))

    if not postForm:
        return jsonify({'Error': 'Empty request body!'}), 400
    # Check the required parameters
    if not 'username' in postForm or not 'password' in postForm or not 'email' in postForm:
        return jsonify({'Error': 'Missing arguments!'}), 400
    # Check if the username exists
    if User.query.filter_by(username=postForm['username']).first() is not None:
        return jsonify({'Error': 'Existing user!'}), 400

    user = User(postForm['username'], pwd_context.encrypt(postForm['password']), postForm['email'])
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({'Error': repr(e)}), 409

    return jsonify({'username': user.username}), 201


@user_auth.verify_password
def verify_password(username, password):
    """
        Verify the user password
    """
    if username:
        user = User.query.get(username)
        if user:
            return pwd_context.verify(password, user.password_hash)
    return False


@user.route('/query', methods=['GET'])
@user_auth.login_required
def query():
    """
        Query all data
    """
    return Data.query_data()


@user.route('/query/<date>', methods=['GET'])
@user_auth.login_required
def query_by_date(date):
    """
        Query data by date
    """
    return Data.query_data(date)


@user.route('/get_daily_report', methods=['GET'])
@user_auth.login_required
def get_daily_report():
    """
        Send an email with a picture that contains a trend of cases and death
    """
    user = User.query.get(user_auth.current_user())
    path = Data.create_picture()
    text = 'Hi {}, this is the latest daily report.'.format(user.username)

    is_successful, message = email_service.send_image(user.email, 'Daily report', text, path)
    if is_successful:  # is_successful=True
        return jsonify({"Info": "Success"}), 200
    else:
        return jsonify({"Error info": str(message)}), 400
