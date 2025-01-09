from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
import secrets
import sqlite3
from flask_session import Session
from test import only_one
from db import db1
from auditor_page import hello
app = Flask(__name__)

# Configuring SQLAlchemy and Flask-Session
# Initialize the Flask-Session extension
app.secret_key = 'hello i am hacker'

# Registering the auditor_page blueprint

app.register_blueprint(hello)

app.register_blueprint(db1)
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use Redis, MongoDB, etc.
Session(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"  # Redirect unauthorized users to login page

# Database helper function to get user data
def get_user_by_username(username):
    query = "SELECT id, username, passwrd,role FROM users_info WHERE username = ?"
    with sqlite3.connect('auditTracker.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        return cursor.fetchone()

# User model
class Users(UserMixin):
    def __init__(self, id, username, passwd,role):
        self.id = id
        self.username = username
        self.passwd = passwd
        self.role=role

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT id, username, passwrd,role FROM users_info WHERE id = ?"
        with sqlite3.connect('auditTracker.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            data = cursor.fetchone()
            if data:
                return cls(id=data[0], username=data[1], passwd=data[2] ,role=data[3])
            return None

@login_manager.user_loader
def load_user(user_id):
    return Users.get_by_id(user_id)

@app.route('/')
def home():
    return render_template('home.html')

# Routes
@app.route('/login_page')
def login_page():
    return render_template('sinin.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    random_str = secrets.token_hex(8)
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = get_user_by_username(username)
        if user_data and user_data[2] == password:
            user = Users(id=user_data[0], username=user_data[1], passwd=user_data[2],role=user_data[3])
            session['username']=username
            session['role']=user_data[3]
            session['islogin']=True
            login_user(user)
            if session['role']=='auditor':
                return redirect(f'/audit1')
            elif session['role']=='admin':
                return redirect(f'/admin1')
            else:
                return 'your are not eligible person'
    return redirect('/login_page')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/admin1')
@login_required
@only_one('admin')
def admin_page():
    return redirect('/admin/admin')

@app.route('/audit1')
@login_required

def audit_checker():
    return redirect('/auditor')

print()
# Run the application
if __name__ == '__main__':
    app.run(debug=True)
