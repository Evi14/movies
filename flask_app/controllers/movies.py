from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_bcrypt import Bcrypt
from datetime import date
bcrypt = Bcrypt(app)

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



@app.route('/favorite/<int:movie_id>/<string:movie_status>')
def addFavoriteMovie(movie_id,movie_status):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id'] ,
        'movie_id': movie_id,
        'movie_status': movie_status

    }
    print(data)
    Movie.addFavoriteMovie(data)
    return redirect(request.referrer)

@app.route('/unfavorite/<int:movie_id>/<movie_status>')
def removeFavoriteMovie(movie_id,movie_status):
    if 'user_id' not in session:
        return redirect('/logout')
    print(movie_id,movie_status)
    data={
        'id': session['user_id'],
        'movie_id': movie_id,
        'movie_status': movie_status

    }
    Movie.removeFavoriteMovie(data)
    return redirect(request.referrer)