from logging import exception

from flask import session, redirect, url_for, request, render_template, flash
from database.select import select_dict
import pymysql
import os
from database.sql_provider import SQLProvider
from . import bp


sql_provide = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@bp.route('/register', methods=['GET'])
def register():
    return render_template('registration.html')

@bp.route('/register', methods=['POST'])
def add_user():
    user_input = request.form
    get_user = sql_provide.get('get_user.sql')
    user_info = select_dict(get_user, user_input)

    if not user_info:
        add_external_user = sql_provide.get('add_user.sql')
        select_dict(add_external_user, user_input)
    else:
        flash('Такой пользователь уже существует!')
        return redirect(url_for('bp_auth.register'))
    return redirect(url_for('bp_auth.auth'))

@bp.route('/', methods=['GET'])
def auth():
    return render_template('auth.html')

@bp.route('/', methods=['POST'])
def check_user():
    user_input = request.form
    user_info = get_user(user_input)
    print("user_info", user_info)
    if user_info:
        user_dict = user_info[0]
        print('user_dict = ', user_dict)
        session['user_id'] = user_dict[0]
        session['user_group'] = user_dict[1]
        session.permanent = True
        return redirect(url_for('main_menu'))
    else:
        return render_template('error_auth.html')

def get_user(user_input):
    get_users = sql_provide.get('get_user.sql')
    user_info = select_dict(get_users, user_input)
    return user_info