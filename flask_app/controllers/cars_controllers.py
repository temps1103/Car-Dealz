from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.car_model import Car




# =================================================
#  Dashboard
# =================================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    # Retrieve the user name
    user_data = {
        'id' : user_id
    }
    user = User.get_by_id(user_data)
    # Retrieve the cars
    cars = Car.get_all_cars()

    return render_template("dashboard.html", user = user, user_id = user_id, cars = cars)

#==================================================
#Route from Dashboard to New Car Page
# =================================================



@app.route("/new/car")
def new_car():
    return render_template("new_car.html")


# ===================================================
# Route from New Car Page to Create New Car
# ===================================================


@app.route("/create/car", methods=["post"])
def create_car():
    # 1 validate form info
    if not Car.validate_car(request.form):
        return redirect("/new/car")
    if 'user_id' not in session:
        flash("Please log in to see this page")
        return redirect('/')
    query_data = {
        "price" : int(request.form["price"]),
        "model" : request.form["model"],
        "make" : request.form["make"],
        "year" : int(request.form["year"]),
        "description" : request.form["description"],        
        "user_id" : session["user_id"]
    }
   
    Car.create_new_car(query_data)
    return redirect("/dashboard")


# =========================================
# Route from Dashboard,One_Car to Delete Car
# =========================================


@app.route("/cars/<int:id>/delete")
def delete_car(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    Car.delete_car(query_data)
    return redirect("/dashboard")


# ========================================
# Route from Dashboard to Edit Car Page
# ========================================

@app.route("/cars/edit/<int:id>")
def edit_car_page(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]
    query_data = {
        "id" : id,
        "user_id" : user_id
    }
    car = Car.get_car_by_id(query_data)
    return render_template("edit_car.html", car = car)

# ============================================
# Route to sumbit Edit from Edit Page
# =============================================

@app.route("/cars/<int:id>/edit", methods=["post"])
def edit_car(id):
    # 1 validate form info
    car_id = request.form["car_id"]
    if not Car.validate_car(request.form):
        return redirect(f"/cars/edit/{car_id}")
   
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    user_id = session["user_id"]     
    query_data = {
        "id" : id,
        "user_id" : user_id,
        "price" : int(request.form["price"]),
        "model" : request.form["model"],
        "make" : request.form["make"],
        "year" : int(request.form["year"]),
        "description" : request.form["description"],
    }
    Car.edit_car(query_data)
    return redirect("/dashboard")




# =====================================
# Route to One Car
# =====================================


@app.route("/cars/<int:id>")
def one_car(id):
    if "user_id" not in session:
        flash("please register or login before going to site")
        return redirect("/")
    query_data = {
        "id" : id
    }
    car = Car.get_car_by_id(query_data)
    return render_template("one_car.html", car = car)