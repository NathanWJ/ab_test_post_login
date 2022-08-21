from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.experiment import Experiment
from flask import flash
import re


class User:
    db = "experiment_db"
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


###################################### 
# CREATE METHODS 
###################################### 

    @classmethod
    def save(cls, data):
        query="INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

###################################### 
# READ METHODS 
###################################### 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data) 
        return cls(results[0])

    @classmethod
    def get_one_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


###################################### 
# VALIDATION METHODS
###################################### 

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL(User.db).query_db(query,user)
        if len(result) >= 1:
            flash("Username already taken.","username")
            is_valid = False
        elif len(user['username']) <1:
            flash("Please add a username.","username")
            is_valid = False

        if len(user['password']) < 1:
            flash("Password can't be blank.","password")
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.","password")
            is_valid = False
        return is_valid


