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
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


    
    @staticmethod
    def is_valid(user):
        is_valid = True
        if not NAME_REGEX.match(user['name']):
            flash("Name should have only letters!", "fnameletter")
            is_valid = False
        if len(user['name']) < 2:
            flash("Name should be at least 2 characters!", "fnamechar")
            is_valid = False
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "email")
            is_valid = False
        query = "select count(email) from users where email = %(email)s;"
        result = connectToMySQL(db_name).query_db(query, user)
        if result[0]['count(email)'] >= 1:
            flash("This email address already exists!", "emailExists")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password should be at least 8 characters!", "password")
            is_valid = False
        # if user['confirm'] != user['password']:
        #     flash("Passwords don't match!", "passwordConfirm")
        #     is_valid = False
        
        if is_valid == True:
            flash("Success, user created!You can now login!", "userCreated")
        
        return is_valid