from flask import Blueprint,render_template

views = Blueprint('views',__name__)

@views.route('/home')
def home():
    return render_template('home_page.html')
    
@views.route('/')
def home_page():
    return render_template("home_page.html")

@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")