from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from .models import engine,sessions,database
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import update,delete,text


auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        phnumber = request.form.get('mobile_number')
        PassWord = request.form.get('Password')
        session.permanent = True
        found_user = sessions.query(database).filter(database.mobile_number == phnumber).first()
        if found_user:
            if check_password_hash(found_user.password, PassWord):
                flash("Logged in successfully", category='success')
                return redirect(url_for('views.dashboard'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Mobile number not register", category='error')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method =='POST':
        mobile_number = request.form.get('number')
        mobile_number = str(mobile_number)
        name = request.form.get('name')
        Password = request.form.get('password')
        confirmPassword = request.form.get('confirm_password')
        user = sessions.query(database).filter(database.mobile_number == mobile_number).first()


        if len(mobile_number) <10:
            flash("Enter 10 digit mobile number", category='error')
        elif len(name) < 2:
            flash("Name must consist above 2 characters", category='error')
        elif confirmPassword!= Password:
            flash("password does not match", category='error')
        elif len(Password) < 8:
            flash("password must be atleast 8 characters", category='error')
        elif user :
            flash("Mobile number already registered", category='error')
        
        else:
            Password = generate_password_hash(Password,method='sha256')
            new_user = database(name=name,mobile_number=mobile_number,password=Password)
            sessions.add(new_user)
            sessions.commit()
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
            

    return render_template("signup.html")

@auth.route('/change', methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        phnumber = request.form.get('mobile_number')
        new_password = request.form.get('new_password')
        name  = request.form.get('name')
        usr = sessions.query(database).filter(database.mobile_number).first()
        if usr:
            pw = sessions.query(database).filter(database.mobile_number == phnumber).first()
            h_pass = generate_password_hash(new_password,method='sha256')
            pw.password = h_pass
            sessions.commit()
            flash("Password changed", category='success')
            return redirect(url_for('auth.login'))
        else:
            flash("User not found please signup", category='error')
    return render_template("change.html")


