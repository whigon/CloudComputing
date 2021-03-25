from Admin import admin
from User import user
from __init__ import app, db

app.register_blueprint(admin, url_prefix='/api/admin')
app.register_blueprint(user, url_prefix='/api/user')

# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
