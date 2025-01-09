from flask_login import current_user
from flask import session ,redirect

def only_one(*role):
    def decorator(func):
        def checker(*arg):
            if not current_user.is_authenticated:
                print(f'i am here.....{current_user["username"]} ')
                return redirect('/login_page')
            if len(role)==2:
                if  session['role'] !=role[0] and session['role'] !=role[1]:
                    print(f'or i am here ... you are {session["role"]} not {role}')
                    print('access denied')
                    return redirect('/login_page')
            elif len(role)==1:
                if session['role']!=role[0]:
                    print(f'your are not admin ,you are {session["role"]}')
                    return redirect('/login_page')
            return func(*arg)
        return checker
    return decorator