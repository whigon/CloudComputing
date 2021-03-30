DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'admin'
PASSWORD = 'mypassword'
HOST = 'database-1.cvuxzz0ptumh.us-east-1.rds.amazonaws.com'
PORT = '3306'
DATABASE = 'Flask'

# mysql URI
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
