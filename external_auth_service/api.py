import json
import os
from base64 import b64decode
from flask import request, jsonify, Flask, render_template, flash, redirect, url_for
from external_auth_service.model_route import model_route
from external_auth_service.database.sql_provider import SQLProvider
from external_auth_service.database.DB_operations import select, insert


service = Flask(__name__)
service.secret_key = '12345'

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

with open('../data/cache_config.json') as f:
    service.config['external_auth_service_config'] = json.load(f)

with open('../data/db_config_client.json') as f:
    service.config['db_config'] = json.load(f)

# @service.route('/external_auth_service/api/auth', methods=['POST'])
@service.route('/external_auth_service/api/auth', methods=['GET'])
def auth():
    if not valid_authorization_request(request):
        return jsonify({'message': 'Bad request'}), 400
    # params = list(request.json.values())
    try:
        params = get_auth_token(request)
    except Exception as e:
        return jsonify({'message': 'except'}), 400

    result_info = model_route(provider, params, 'get_user.sql', select)

    if result_info.status:
        return jsonify({'message': 'Successful authorization', 'user_id': result_info.result}), 200
    else:
        return jsonify({'message': 'User not found'}), 400

@service.route('/external_auth_service/register', methods=['GET'])
def input_register():
    return render_template('register.html')

@service.route('/external_auth_service/api/register', methods=['POST'])
def register():
    login = request.form.get('login')
    result_user_info = model_route(provider, [login], 'check_user.sql', select)

    if not result_user_info.status:
        params = list(request.form.values())
        print("params: ", params)
        result_info = model_route(provider, params, 'add_user.sql', insert)

        # if result_info.status:
        #     message = 'Successful registration'
        # else:
        #     message = 'Failed registration'

        # url = 'http://127.0.0.1:8080/auth/'
        # response = requests.post(url, 'message': message)
        return redirect('http://127.0.0.1:8080/auth/')

    else:
        flash('Такой пользователь уже существует!')
        return redirect(url_for('input_register'))

def get_auth_token(api_request)-> list:
    header = api_request.headers.get('Authorization')
    token = header.split()[-1]
    params = b64decode(token.encode('ascii')).decode('ascii').split(':')
    print('params: ', params)
    if len(params) != 2:
        raise ValueError('Invalid login or password')
    return params

def valid_authorization_request(api_request):
    header = api_request.headers.get('Authorization')
    if not header:
        return False
    if not header.startswith('Basic '):
        return False
    if len(header) <= len('Basic '):
        return False
    return True

if __name__ == '__main__':
    service.run(host='127.0.0.1', port=5000)

