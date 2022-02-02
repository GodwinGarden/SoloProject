from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.garden import Garden
from flask_app.models.visitor import Visitor


@app.route('/new/garden')
def new_garden():
    if 'visitor_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['visitor_id']
    }
    return render_template('new_garden.html', visitor=Visitor.get_by_id(data))


@app.route('/create/garden',methods=['POST'])
def create_garden():
    if 'visitor_id' not in session:
        return redirect('/logout')
    if not Garden.validate_garden(request.form):
        return redirect('/new/garden')
    data = {
        "garden_name": request.form["garden_name"],
        # "category": request.form["category"],
        "web_page": request.form["web_page"],
        "city": request.form["city"],
        "country": request.form["country"],
        "comments": request.form["comments"],
        # "visited": request.form["visited"],
        # "favorite": request.form["favorite"],
        "visitor_id": session["visitor_id"]
    }
    Garden.save(data)
    return redirect('/dashboard')

@app.route('/update/garden/<int:id>')
def edit_garden(id):
    if 'visitor_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    visitor_data = {
        "id":session['visitor_id']
    }
    return render_template("edit_garden.html",edit=Garden.get_one(data),visitor=Visitor.get_by_id(visitor_data))

@app.route('/update/garden',methods=['POST'])
def update_garden():
    if 'visitor_id' not in session:
        return redirect('/logout')
    if not Garden.validate_garden(request.form):
        return redirect(f"/edit/garden/{request.form['id']}")
    data = {
        "garden_name": request.form["garden_name"],
        "web_page": request.form["web_page"],
        "city": request.form["city"],
        "country": request.form["country"],
        "comments": request.form["comments"],
        "id": request.form['id']
        }
    Garden.update(data)
    return redirect('/dashboard')

@app.route('/garden/<int:id>')
def show_garden(id):
    if 'visitor_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
        }
    visitor_data = {
        "id":session['visitor_id']
        }
    return render_template("garden.html",garden=Garden.get_one(data), logged_in_user=Visitor.get_by_id(visitor_data))

@app.route('/destroy/garden/<int:id>')
def destroy_garden(id):
    if 'visitor_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
        }
    Garden.destroy(data)
    return redirect('/dashboard')