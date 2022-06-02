from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.car_model import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)





@app.route("/")
def index():
    return render_template("index.html")


    

# ============================================================
# Registure Route
# ============================================================


@app.route("/register", methods = ["post"])
def new_user():
    # 1 validate form info
    if not User.validate_register(request.form):
        return redirect("/")
    # 2 side - convert password via bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    # 2 collect data from form
    query_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash,
    }
    # 3 run query to database (INSERT)
    session["user_id"] = User.create_user(query_data)
    #3a add user id to session
    # 4 redirect elsewhere
    return redirect("/dashboard")



    # ============================================================
# Login Route
# ============================================================

@app.route("/login", methods = ["post"])
def login():
    #1 validate info
    if not User.validate_login(request.form):
        return redirect("/")
    #2 query based on data
    query_data = {
        "email" : request.form["email"]    
    }
    logged_in_user = User.get_by_email(query_data)
    #3 put user_id into session
    session["user_id"] = logged_in_user.id
    #4 redirect elsewhere

    return redirect("/dashboard")





    
# ==================================================
# Logout
# ==================================================

@app.route("/logout")
def logout():    
    session.clear()
    return redirect("/")
