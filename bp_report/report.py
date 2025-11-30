from . import bp
import os
import json
from flask import render_template, request, redirect, url_for, flash
from .model_route import model_route
from database.DB_operations import call_proc, select
from database.sql_provider import SQLProvider
from bp_auth.access import group_require


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@bp.route('/', methods=['GET'])
@group_require
def report_menu():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'json', 'report_params.json')

    with open(file_path, encoding='utf-8') as file:
        report_params = json.load(file)

    return render_template("report_menu.html", report_params=report_params)

@bp.route('/param_input', methods=['POST'])
def param_input():
    # print(request.form)
    params = request.form
    return render_template("param_input.html", params=params)

@bp.route('/get_report', methods=['POST'])
@group_require
def get_report():
    params = [request.form.get('year'), request.form.get('month')]
    result_info = model_route(provider, params, 'get_report.sql', request.form['name_report'], select)

    if result_info.status:
        col_headers_file = request.form.get('col_headers_file')
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'json', col_headers_file)

        with open(file_path, encoding='utf-8') as file:
            col_headers = json.load(file)

        return render_template("dynamic_get_report.html", name_cols=col_headers, data_results=result_info.result)
    else:
        return render_template("no_reports.html")

@bp.route('/add_report', methods=['POST'])
@group_require
def add_report():
    user_input = request.form
    params = [user_input.get('year'), user_input.get('month')]
    result_info = model_route(provider, params, 'сreate_report.sql', user_input['name_procedure'], call_proc)

    if result_info.status:
        print(result_info.result)
        for messages in result_info.result:
            for message in messages:
                print(message)
                flash(message)

    return redirect(url_for('bp_report.report_menu'))
