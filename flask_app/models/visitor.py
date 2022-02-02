from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
import re	
  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Visitor:
    db = "visitors_gardens"
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.paintings = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def save(cls,data):
        query = "INSERT INTO visitors (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM visitors;"
        results = connectToMySQL(cls.db).query_db(query)
        visitors = []
        for row in results:
            visitors.append(cls(row))
        return visitors

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM visitors WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM visitors WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE visitors SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def edit_visitor(visitor):
        is_valid = True
        query = "SELECT * FROM visitors WHERE email = %(email)s;"
        results = connectToMySQL(Visitor.db).query_db(query,visitor)
        one_visitor=Visitor.get_by_email({"email":visitor["email"]})
        logged_user=Visitor.get_by_id({"id":session["visitor_id"]})
        print (one_visitor.email)
        print (logged_user.email)
        if one_visitor: 
            if one_visitor.email == logged_user.email:

                # if len(results) >= 1:
                flash("Email already in use","register")
                is_valid=False
        if not EMAIL_REGEX.match(visitor['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(visitor['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(visitor['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(visitor['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        # if visitor['password'] != visitor['confirm']:
        #     flash("Passwords don't match","register")
        return is_valid

    @staticmethod
    def validate_register(visitor):
        is_valid = True
        query = "SELECT * FROM visitors WHERE email = %(email)s;"
        results = connectToMySQL(Visitor.db).query_db(query,visitor)
        if len(results) >= 1:
            flash("Email already in use","register")
            is_valid=False
        if not EMAIL_REGEX.match(visitor['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(visitor['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(visitor['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(visitor['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if visitor['password'] != visitor['confirm']:
            flash("Passwords don't match","register")
        return is_valid