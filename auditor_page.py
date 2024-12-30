from flask import Flask , render_template , url_for , redirect,request,abort, Blueprint
hello=Blueprint(__name__ ,'auditor')
@hello.route('/auditor')
def auditor_page():
    return 'hello auditor'
auditor_page()