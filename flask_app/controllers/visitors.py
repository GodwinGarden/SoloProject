from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.visitor import Visitor
from flask_app.models.garden import Garden
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not Visitor.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        }
    id = Visitor.save(data)
    session['visitor_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    visitor = Visitor.get_by_email(request.form)

    if not visitor:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(visitor.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['visitor_id'] = visitor.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'visitor_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['visitor_id']
        }
    return render_template("dashboard.html",visitor=Visitor.get_by_id(data),gardens=Garden.get_all_with_visitors())

@app.route('/update/visitor/<int:id>')
def edit_visitor(id):
    if 'visitor_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    visitor_data = {
        "id":session['visitor_id']
    }
    return render_template("edit_profile.html",edit=Visitor.get_by_id(data),visitor=Visitor.get_by_id(visitor_data))


@app.route('/update/visitor',methods=['POST'])
def update_visitor():
    if 'visitor_id' not in session:
        return redirect('/logout')
    if Visitor.edit_visitor(request.form):
        return redirect(f"/update/visitor/{request.form['id']}")
        # return redirect(f"edit_profile/{request.form['id']}")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "id": request.form['id']
        }
    Visitor.update(data)
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')