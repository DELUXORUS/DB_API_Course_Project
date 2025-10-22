from flask import Flask, render_template, session
import json
import os
from bp_auth.access import login_require
from bp_request import bp as bp_request
from bp_auth import bp as bp_auth

app = Flask(__name__)
app.secret_key = '1234'

app.register_blueprint(bp_request, url_prefix='/requests')
app.register_blueprint(bp_auth, url_prefix='/auth')

with open('../data/db_config_root.json') as f:      #открываем db_config_root.json
    app.config['db_config'] = json.load(f)      #загружаем содержимое файла, with его сам закрывает
with open('../data/db_access.json') as f:
    app.config['db_access'] = json.load(f)

#Декоратор - функция, которая принимает другую функцию. Внутри декоратора есть функция, которая называется - обёртка оборачивает декорируемую функцию и реализует дополнительную функциональность
#Чтобы передать функцию в аргументе декоратора, достаточно указать ее имя. Чтобы вернуть функцию, достаточно указать ее имя.
@app.route('/')
@login_require
def main_menu():
    user_group = session['user_group']
    base_dir = os.path.dirname(os.path.dirname(__file__))
    name_file = 'db_config_' + user_group + '.json'
    print (name_file)
    file_path = os.path.join(base_dir, 'data', name_file)

    with open(file_path) as f:  # открываем db_config.json
        app.config['db_config'] = json.load(f)  # загружаем содержимое файла, with его сам закрывает

    return render_template("main.html")

@app.route('/shutdown')
def shutdown_program():
    session.clear()
    with open('../data/db_config_root.json') as f:  # открываем db_config_root.json
        app.config['db_config'] = json.load(f)
    return render_template("shutdown.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)