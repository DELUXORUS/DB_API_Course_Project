import os
import json
from flask import render_template, request
from database.sql_provider import SQLProvider
from database.DB_operations import select
from .model_route import model_route
from . import bp
from bp_auth.access import group_require


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# print("os_path = ", os.path)
# print("dirname = ", os.path.dirname(__file__))

@bp.route('/', methods=['GET'])
@group_require
def query_menu():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'json', 'request_params.json')

    with open(file_path, encoding='utf-8') as file:
        request_params = json.load(file)

    return render_template("query_menu.html", request_params=request_params)

@bp.route('/input_handler', methods=['GET'])
def input_handler():
    html_file = request.args.get('html_file')
    return render_template(html_file)

@bp.route('/result', methods=['POST'])
def result_handler():
    user_input = request.form
    filtered_dict = {k: v for k, v in user_input.items() if k not in ("col_headers_file", "sql_file")}
    params = list(filtered_dict.values())

    result_info = model_route(provider, params, user_input["sql_file"], select)

    if result_info.status:
        col_headers_file = request.form.get('col_headers_file')
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'json', col_headers_file)
        with open(file_path, encoding='utf-8') as file:
            col_headers = json.load(file)

        return render_template("dynamic_result.html", name_cols=col_headers, data_results=result_info.result, title='Результат параметризированного запроса')
    else:
        return render_template("wrong.html")