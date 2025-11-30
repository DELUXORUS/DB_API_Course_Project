import requests
import os
import json
from base64 import b64encode
from flask import session, redirect, url_for, request, render_template, current_app
from database.DB_operations import select
from database.sql_provider import SQLProvider
from .model_route import model_route
from . import bp


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@bp.route('/', methods=['GET'])
def auth():
    return render_template('auth.html')

@bp.route('/', methods=['POST', 'GET'])
def check_user():
    user_input = request.form
    params = list(user_input.values())
    internal_user_info_pack = model_route(provider, params, 'get_user.sql', select)
    internal_user_info = internal_user_info_pack.result
    print("internal_user_info: ", internal_user_info)

    if internal_user_info:
        user_info = internal_user_info[0]
        # print('user_dict = ', user_info)
        session['user_id'] = user_info[0]
        session['user_group'] = user_info[1]

        db_config = user_info[2]
        with open(f'../data/{db_config}') as f:  # открываем db_config_root.json
            current_app.config['db_config'] = json.load(f)

        return redirect(url_for('main_menu')) if internal_user_info else render_template('error_auth.html')
    else:
        base_url = 'http://127.0.0.1:5000/external_auth_service/api'
        url = f'{base_url}/auth'
        login = user_input['login']
        password = user_input['password']
        # data = {'login': user_input['login'], 'password': user_input['password']}

        # response = requests.post(url, json=data)
        response = requests.get(url, headers={'Authorization': create_basic_auth_token(login, password)})
        status = response.status_code
        response_json = response.json()

        with open('../data/db_config_client.json') as f:  # открываем db_config_root.json
            current_app.config['db_config'] = json.load(f)

        if status == 200:
            session['user_group'] = "client"
            session['user_id'] = response_json['user_id']
            session.permanent = True
            return redirect(url_for('main_menu'))
        else:
            # return render_template('error_auth.html')
            return response_json

def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    ccc = b64encode(f'{login}:{password}'.encode('ascii'))
    print('ccc: ', ccc)
    print('credentials_b64: ', credentials_b64)
    token = f'Basic {credentials_b64}'
    return token