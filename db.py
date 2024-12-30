from flask import Flask ,render_template, redirect ,request ,abort,url_for,Blueprint
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
import sqlite3
db=Blueprint(__name__,'admin_db')
@db.route('/admin')
def admin_access():
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        sql=f'''select * from password '''
        pointer.execute(sql)
        data=pointer.fetchall()
        for i in data:
            print(i)
        with app.app_context():
            return render_template('admin.html',datas=data)
    except sqlite3.OperationalError as e:
        return str(e)
    finally:
        conn.commit()
admin_access()
