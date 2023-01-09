from flask_app import app
# importo modelet dhe kontrollet
from flask_app.models.user import User
from flask_app.controllers import users
# from flask_app.models.ninja import Ninja
# from flask_app.controllers import ninjas

if __name__ == "__main__":
    app.run(debug=True)