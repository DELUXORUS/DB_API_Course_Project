from flask import Flask, render_template, session
import json
from bp_auth.access import login_require
from bp_request import bp as bp_request
from bp_auth import bp as bp_auth
from bp_report import bp as bp_report
from bp_order import bp as bp_order

app = Flask(__name__)
app.secret_key = '1234'

app.register_blueprint(bp_request, url_prefix='/requests')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_report, url_prefix='/report')
app.register_blueprint(bp_order, url_prefix='/order')

with open('../data/db_config_root.json') as f:      #открываем db_config_root.json
    app.config['db_config'] = json.load(f)      #загружаем содержимое файла, with его сам закрывает
with open('../data/db_access.json') as f:
    app.config['db_access'] = json.load(f)
with open('../data/cache_config.json') as f:  # открываем db_config_root.json
    app.config['cache_config'] = json.load(f)

    #Декоратор - функция, которая принимает другую функцию. Внутри декоратора есть функция, которая называется - обёртка оборачивает декорируемую функцию и реализует дополнительную функциональность
#Чтобы передать функцию в аргументе декоратора, достаточно указать ее имя. Чтобы вернуть функцию, достаточно указать ее имя.
@app.route('/')
@login_require
def main_menu():
    db_access = app.config['db_access']
    user_group = session['user_group']
    current_access = db_access[user_group]
    # print("db_access: ", db_access)
    # print("user_group: ", user_group)
    # print("current_access: ", current_access)

    with open('./json/blueprints_access.json', encoding='utf-8') as f:  # открываем db_config_root.json
        blueprints = json.load(f)

    print("blueprints: ", blueprints)
    filtered_values = [blueprints[key] for key in current_access if key in blueprints]

    return render_template("main.html", blueprints = filtered_values)

@app.route('/shutdown')
def shutdown_program():
    session.clear()
    with open('../data/db_config_root.json') as f:  # открываем db_config_root.json
        app.config['db_config'] = json.load(f)
    return render_template("shutdown.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)