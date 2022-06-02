from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Car:
    db = "car_dealz_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]              
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = {}



    @staticmethod
    def validate_car(form_data):
        is_valid = True

        
        if len(form_data["price"]) <= 0:
            flash("Please enter a valid price")
            is_valid = False
            
        elif int(form_data["price"]) <= 0:
            flash("Price must be greater than 0")
            is_valid = False        
        
        if len(form_data["model"]) < 2:
            flash("Model must be 2 characters long")
            is_valid = False

        if len(form_data["make"]) < 2:
            flash("Make must be 2 characters long")
            is_valid = False
               
        if len(form_data["year"]) <= 0:
            flash("Please enter a valid year")
            is_valid = False
        
        elif int(form_data["year"]) <= 1900:
            flash("Year can't be older than 1900")
            is_valid = False
            
        if len(form_data["description"]) < 10:
            flash("Description must be 10 characters long")
            is_valid = False          
        
      
        return is_valid





    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        user_all_cars = []
        for dict in results:
            user_cars = cls(dict)
            user_data = {
                'id' : dict['users.id'],
                'first_name' : dict["first_name"],
                'last_name' : dict["last_name"],
                'email' : dict["email"],
                'password' : dict["password"],
                'created_at' : dict["users.created_at"],
                'updated_at' : dict["users.updated_at"]
            }

            user_cars.user = user_model.User(user_data)
            user_all_cars.append(user_cars)

        return user_all_cars



    @classmethod
    def create_new_car(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, created_at, updated_at, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results



    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @classmethod
    def get_car_by_id(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        car = cls(results[0])
        user_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]["first_name"],
            'last_name' : results[0]["last_name"],
            'email' : results[0]["email"],
            'password' : results[0]["password"],
            'created_at' : results[0]["users.created_at"],
            'updated_at' : results[0]["users.updated_at"]
        }

        car.user = user_model.User(user_data)
        
        return car
 

    @classmethod
    def edit_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, updated_at = now() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results