from flask import render_template,redirect,session,request, flash, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models import user
from flask_app.models import movie
from flask_bcrypt import Bcrypt
from datetime import date
bcrypt = Bcrypt(app)

import os
import re
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import uuid as uuid
UPLOAD_FOLDER = 'flask_app/static/assets/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    movies  = User.get_all_movies()
    clebrities = User.get_celebrities()
    return render_template('index.html', movies = movies, clebrities = clebrities)


@app.route('/celebrities')
def celebrities():
    celebrities = User.get_celebrities()
    return render_template('celebrities.html', celebrities = celebrities)


@app.route('/celebritiesAdmin')
def celebritiesAdmin():
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    print(user.role)
    if user.role == "admin":
        celebrities = User.get_celebrities()
        return render_template('celebAdmin.html', celebrities = celebrities)
    else:
        return redirect('/logout')


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
    if user_in_db.role == 'admin':
        return redirect("/admin")
    else:return redirect("/dashboard")


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
    movies  = User.get_all_movies()
    clebrities = User.get_celebrities()
    return render_template("loggedUser.html",user=User.get_by_id(data), movies = movies, clebrities = clebrities)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

#ELDI

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    print(user.role)
    if user.role != "admin":
        return redirect('/logout')
    movies  = User.get_all_movies()
    return render_template('admin.html', user = user, movies = movies)

@app.route('/create_movie', methods = ['POST'])
def create_movie():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect('/logout')
    data['title'] = request.form['title']
    data['description'] = request.form['description']
    # data['cover_pic'] = request.form['cover_pic']
    data['release_date'] = request.form['release_date']
    data['trailer'] = request.form['trailer']
    data['writer'] = request.form['writer']
    data['director'] = request.form['director']
    data['movie_profile'] = request.form['movie_profile']
    data['duration'] = request.form['duration']
    data['status'] = request.form['status']
    # data['video'] = request.form['video']
    file = request.files['cover_pic']
    if file and allowed_file(file.filename):
        pic_filename = secure_filename(file.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        # data = {
        #     'file_path': pic_name,
        #     'dev_id': session['user_id']
        # }
        data['cover_pic'] = pic_name
    print(data)
    User.create_movie(data)
    return redirect(request.referrer)

@app.route('/movie_detail/<int:id>')
def movie_detail(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect('/logout')
    data['movie_id'] = id
    movie = User.get_movie_by_id(data)
    comments = User.get_movie_comments(data)
    users = []
    comment_details = []
    for comment in comments:
        data['id'] = comment['user_id']
        the_user = User.get_by_id(data)
        detail = {
            'user': the_user['name'],
            'comment': comment['comment']
        }
        comment_details.append(detail)
    return render_template('movie-details.html', user = user, movie = movie, users = users, comment_details = comment_details)

@app.route('/editMovie/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect('/logout')
    
    data['movie_id'] = id
    movie = User.get_movie_by_id(data)
    if movie == False:
        return redirect(request.referrer)
    return render_template('editMovie.html', user = user, movie = movie)

@app.route('/updateMovie/<int:id>', methods = ['POST'])
def updateMovie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'movie_id': id
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect('/logout')
    movie = User.get_movie_by_id(data)
    data['title'] = request.form['title']
    data['release_date'] = request.form['release_date']
    data['trailer'] = request.form['trailer']
    data['writer'] = request.form['writer']
    data['director'] = request.form['director']
    data['movie_profile'] = request.form['movie_profile']
    data['duration'] = request.form['duration']
    if data['title'] == '':
        data['title']=movie['title']
    elif data['release_date'] == '':
        data['release_date'] = movie['release_date']
    elif data['trailer']=='':
        data['trailer']= movie['trailer']
    elif data['writer'] == '':
        data['writer'] = movie['writer']
    elif data['director'] == '':
        data['director'] = movie['director']
    elif data['movie_profile'] == '':
        data['movie_profile'] = movie['profile']
    elif data['duration'] == '':
        data['duration'] = movie['duration']
    
    if request.files['cover_pic']:
        file = request.files['cover_pic']
        if file and allowed_file(file.filename):
            pic_filename = secure_filename(file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            data['cover_pic'] = pic_name
    else:
        data['cover_pic'] = movie['cover_pic']
    User.updateMovie(data)
    return redirect(request.referrer)

@app.route('/addComment/<int:movie_id>', methods = ['POST'])
def addComment(movie_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
        'movie_id': movie_id,
        'comment': request.form['comment']
    }
    User.addComment(data)
    return redirect(request.referrer)

@app.route('/aboutUs')
def aboutUs():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('aboutUs.html')


@app.route('/top-movies')
def topMovies():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id':session['user_id']
    }
    movies=Movie.get_movie()
    today = date.today()
    fav=Movie.get_user_favorite_movies(data)
    rated=Movie.get_rated_movies()
    coming=Movie.get_coming_movies()
    favMoviesId=Movie.get_user_favorite_moviesID(data)
    return render_template('top-movies.html', movies=movies, fav=fav, rated=rated,coming=coming, favMoviesId=favMoviesId)


@app.route('/addCelebrities/<int:movie_id>', methods = ['POST'])
def addCelebrities(movie_id):
    if 'user_id' not in session:
            return redirect('/logout')
    data ={
        'id': session['user_id'],
        'movie_id': movie_id,
        'name': request.form['name']
    }
    user = User.get_by_id(data)
    if user.role != "admin":
        return redirect('/logout')
    file = request.files['profile_pic']
    if file and allowed_file(file.filename):
        pic_filename = secure_filename(file.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        data['profile_pic'] = pic_name
    User.addCelebrities(data)
    return redirect(request.referrer)

    
