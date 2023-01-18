from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db_name = 'movie'
class User:
    db_name = "movie"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.profile_pic = data['profile_pic']
        self.credit = data['credit']
        self.role = data['role']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,email,password, role) VALUES(%(name)s,%(email)s,%(password)s,'user')"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getUserEmail(cls):
        query = "SELECT email FROM users;"
        result = connectToMySQL(cls.db_name).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]
    
    #ELDI
    
    @classmethod 
    def create_movie(cls, data):
        query = "INSERT INTO movies (title, description, writer, director, release_date, trailer, duration, profile, cover_pic, status) VALUES (%(title)s, %(description)s, %(writer)s, %(director)s, %(release_date)s, %(trailer)s, %(duration)s, %(movie_profile)s, %(cover_pic)s, %(status)s);"
        print(query)
        connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod 
    def get_all_movies(cls):
        query = "SELECT * FROM movies ORDER BY created_at DESC;"
        result = connectToMySQL(cls.db_name).query_db(query)
        movies = []
        for row in result:
            movies.append(row)
        print(movies[0]['title'])
        return movies
    
    @classmethod
    def get_movie_by_id(cls, data):
        query = "SELECT * FROM movies WHERE id = %(movie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        else:
            return False

    @classmethod
    def updateMovie(cls, data):
        query = "UPDATE movies SET title = %(title)s, writer = %(writer)s, director = %(director)s, release_date = %(release_date)s, trailer = %(trailer)s, duration = %(duration)s, profile = %(movie_profile)s, cover_pic = %(cover_pic)s WHERE id = %(movie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (user_id, movie_id, comment) VALUES (%(id)s, %(movie_id)s, %(comment)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_movie_comments(cls, data):
        query = "SELECT * FROM comments WHERE movie_id = %(movie_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        for row in result:
            comments.append(row)
        return comments

    @classmethod
    def addCelebrities(cls, data):
        query = "INSERT INTO celebrities (movie_id, name, profile_pic) VALUES (%(movie_id)s, %(name)s, %(profile_pic)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_celebrities(cls):
        query = "SELECT * FROM celebrities LEFT JOIN movies ON celebrities.movie_id = movies.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        celebrities = []
        for row in result:
            celebrities.append(row)
        # print(celebrities)
        return celebrities

    @classmethod
    def book_tickets(cls, data):
        query = "INSERT INTO tickets_booked (seat, user_id, movie_id) VALUES (%(seat)s, %(id)s, %(movie_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def is_valid(user):
        is_valid = True
        query = "select count(email) from users where email = %(email)s;"
        result = connectToMySQL(db_name).query_db(query, user)
        if result[0]['count(email)'] >= 1:
            # flash("This email address already exists!", "emailExists")
            is_valid = False
        # if is_valid == True:
            # flash("Success, user created!You can now login!", "userCreated")
        return is_valid