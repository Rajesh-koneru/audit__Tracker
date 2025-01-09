from flask import Flask , render_template , url_for , redirect,request,abort, Blueprint
from flask_login import login_required
from test import only_one
hello=Blueprint(__name__ ,'auditor')
@hello.route('/auditor')
@login_required
@only_one('admin','auditor')
def auditor_page():
    return 'hello auditor'