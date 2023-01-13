from flask import render_template,redirect,session,request, flash, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/celebrities')
def celebrities():
    return render_template('celebrities.html')


@app.route('/login', methods=['POST'])
def login():
    # if User.is_valid(request.form):
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "invalidEmail")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "loginPassError")
        return redirect(request.referrer)
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route('/register', methods=['POST'])
def register():
    if User.is_valid(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # print(pw_hash)
        data = {
                "name": request.form['name'],
                "email": request.form['email'],
                "password" : pw_hash
        }
        id = User.save(data)
        session['user_id'] = id
        return redirect("/dashboard")
    return redirect("/")

@app.route('/getUser')
def getUser():
    emails = user.User.getUserEmail()
    return jsonify(emails)


@app.route('/getUserLogin')
def getUserLogin():
    emails = user.User.getUserEmail()
    return jsonify(emails)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("loggedUser.html",user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")