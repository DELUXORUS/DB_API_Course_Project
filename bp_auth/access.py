from functools import wraps
from flask import session, redirect, url_for, current_app, request, render_template


def login_require(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('bp_auth.auth'))
    return wrapper

def group_require(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            access = current_app.config['db_access']
            user_role = session.get('user_group')
            user_request = request.endpoint.split('.')[0]
            print('request.endpoint', request.endpoint)
            print('user_request', user_request)
            if user_role in access and user_request in access[user_role]:
                return func(*args, **kwargs)
            else:
                return render_template('no_access.html')
        return 'Необходимо авторизоваться'
    return wrapper
