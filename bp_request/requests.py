import os
import json
from flask import render_template, request
from database.sql_provider import SQLProvider
from .model_route import model_route
from . import bp
from bp_auth.access import group_require

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
print("os_path = ", os.path)
print("dirname = ", os.path.dirname(__file__))

#Хэндлер, который для выбора типа запроса, после чего тип запроса отправляется в result_handler

@bp.route('/', methods=['GET'])
@group_require
def query_menu():
    return render_template("query_menu.html")

@bp.route('/input_handler', methods=['GET'])
def input_handler():
    html_file = request.args.get('html_file')
    return render_template(html_file)

# @bp.route('/input_num_days', methods=['GET'])
# def input_num_days():        #Показать все сведения о клиентах, заключивших договора за последение N дней
#     return render_template("input_num_days.html")
#
# @bp.route('/input_unique_code', methods=['GET'])
# def input_unique_code():      #Определить максимальну цену для услуг, уникальный код которых начинается с XXX
#     return render_template("input_unique_code.html")

@bp.route('/result', methods=['POST'])
def result_handler():
    user_input = request.form
    print("request.form = ", user_input)

    col_headers_file = request.form.get('col_headers_file')
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'col_headers', col_headers_file)

    with open(file_path, encoding='utf-8') as file:
        col_headers = json.load(file)

    result_info = model_route(provider, user_input)
    if result_info.status:
        data_results = result_info.result
        title = 'Результат параметризированного запроса'
        return render_template("dynamic_result.html", name_cols=col_headers, data_results=data_results, title=title)
    else:
        return render_template("wrong.html")