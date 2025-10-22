from .DB_context_manager import DBContextManager
from flask import current_app

def select_list(_sql: str, param_list: list) -> tuple:
    with DBContextManager(current_app.config['db_config']) as cursor:   #with DBContextManager(...) -> __init__ -> enter -> as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')  #генерируем (c помощью ValueError) ошибку чтобы вернуться в exit
        else:
            cursor.execute(_sql, param_list)    #двухфазое выполнение запроса
            result = cursor.fetchall()
            return result   #где то error или return в конце -> __exit__ -> return (тк exit возвращает управление туда откуда его вызвали)

#когда кому передавать управление знает with (поэтому эти 3 метода обязательны (init, enter, exit))

def select_dict(_sql, user_input: dict) -> tuple:
    user_list = []
    for key in user_input:
        if "file" not in key:
            user_list.append(user_input[key])
    print("user_list = in dict",user_list)
    result = select_list(_sql, user_list)
    return result