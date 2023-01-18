from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Movie:
    db_name = "movie"


    @classmethod
    def get_movie(cls):
            query = "SELECT * FROM movies order by created_at DESC;"
            results =  connectToMySQL(cls.db_name).query_db(query)
            movies= []
            for row in results:
                print(row)
                movies.append(row)
            return movies

    @classmethod
    def addFavoriteMovie(cls, data):
        print(data)
        query= 'INSERT INTO favorite_movies (movie_id,user_id, status) VALUES ( %(movie_id)s, %(id)s, %(movie_status)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeFavoriteMovie(cls, data):
        query= 'DELETE FROM favorite_movies WHERE movie_id = %(movie_id)s and user_id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_favorite_movies(cls, data):
        query = 'SELECT   favorite_movies.id, favorite_movies.user_id, favorite_movies.movie_id as movie_id, movies.title,movies.description , movies.writer, movies.director,movies.release_date, movies.trailer,movies.cover_pic,movies.video, movies.status FROM  favorite_movies JOIN  users on favorite_movies.user_id = users.id  JOIN movies on favorite_movies.movie_id = movies.id where favorite_movies.user_id=%(user_id)s order by movies.release_date DESC ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersFavorite = []
        for row in results:
            usersFavorite.append(row)
        return usersFavorite
    @classmethod
    def get_user_favorite_moviesID(cls, data):
        query = 'SELECT   favorite_movies.movie_id as movie_id   FROM  favorite_movies JOIN  users on favorite_movies.user_id = users.id  JOIN movies on favorite_movies.movie_id = movies.id where favorite_movies.user_id=%(user_id)s order by movies.release_date DESC ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        Favorite = []
        for row in results:
            Favorite.append(row['movie_id'])
        return Favorite

    @classmethod
    def get_coming_movies(cls):
        query = 'SELECT   * FROM  movies where status= "0" order by created_at DESC;'
        results = connectToMySQL(cls.db_name).query_db(query)
        comingMovies = []
        for row in results:
            comingMovies.append(row)
        return comingMovies

    @classmethod
    def get_rated_movies(cls):
        query = 'SELECT   movies.title, movies.id as id, movies.status, movies.description, movies.cover_pic,movies.trailer, COUNT(favorite_movies.id) as mostliked  FROM  movies JOIN favorite_movies on favorite_movies.movie_id=movies.id  GROUP BY movies.id order by favorite_movies.id AND movies.release_date DESC;'
        results = connectToMySQL(cls.db_name).query_db(query)
        ratedMovies = []
        for row in results:
            ratedMovies.append(row)
        return ratedMovies
