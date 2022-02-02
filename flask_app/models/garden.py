from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import visitor


class Garden:
    db_name = 'visitors_gardens'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.garden_name = db_data['garden_name']
        # self.category = db_data['category']
        self.web_page = db_data['web_page']
        self.city = db_data['city']
        self.country = db_data['country']
        self.comments = db_data['comments']
        # self.visited = db_data['visited']
        # self.favorite = db_data['favorite']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.visitor_id = db_data['visitor_id']
        self.visitor = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO gardens (garden_name, web_page, city, country, comments, visitor_id) VALUES (%(garden_name)s,%(web_page)s,%(city)s,%(country)s,%(comments)s,%(visitor_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gardens;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_gardens = []
        for row in results:
            print(row['garden_name'])
            all_gardens.append(cls(row))
        return all_gardens

    @classmethod
    def get_all_with_visitors(cls):
        query = "SELECT * FROM gardens JOIN visitors ON visitors.id = visitor_id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_gardens = []
        for row in results:
            this_garden = cls(row)
            visitor_dict = {
                'id':row['visitors.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['visitors.created_at'],
                'updated_at':row['visitors.updated_at']
            }
            this_visitor = visitor.Visitor(visitor_dict)
            this_garden.visitor = this_visitor
            all_gardens.append(this_garden)
        return all_gardens
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM gardens JOIN visitors on visitors.id = visitor_id WHERE gardens.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        this_garden=cls(results[0])
        # need to create a dictionary {} for each get_one
        visitor_dict = {
            'id':results[0]['visitors.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['visitors.created_at'],
            'updated_at':results[0]['visitors.updated_at']
        }      
        this_visitor=visitor.Visitor(visitor_dict)
        this_garden.visitor=this_visitor 
        return this_garden


    @classmethod
    def update(cls, data):
        query = "UPDATE gardens SET garden_name=%(garden_name)s, web_page=%(web_page)s, city=%(city)s, country=%(country)s, comments=%(comments)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM gardens WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_garden(garden):
        is_valid = True
        if len(garden['garden_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","garden")
        # if len(garden['category']) < 3:
        #     is_valid = False
        #     flash("Please choose a category","garden")
        if len(garden['comments']) < 3:
            is_valid = False
            flash("Please submit comments to help other visitors","garden")
        return is_valid