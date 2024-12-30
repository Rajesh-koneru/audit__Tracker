from flask import Flask , render_template , url_for , redirect,request,abort
import sqlite3
from auditor_page import hello
app=Flask(__name__)
app.register_blueprint(hello)
from db import db
app.register_blueprint(db,)
@app.route('/')
def login_page():
    return render_template('sinin.html')
@app.route('/login',methods=['POST', 'GET'])
def login():
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        user=request.form.get('username')
        passwrd=request.form.get('password')
        sql=f'''select * from password where name='{user}' and  passwrd={passwrd}; '''
        pointer.execute(sql)
        data =pointer.fetchone()
        if request.method=="POST":
            if data and data[1] == user and data[2]==passwrd:
                return redirect(f'/{user}')
            else:
                abort(400)
    except sqlite3.OperationalError as e:
        return str(e)
    finally:
        conn.close()
if __name__=='__main__':
    app.run()




