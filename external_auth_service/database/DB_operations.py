from .DB_context_manager import DBContextManager
from flask import current_app


def select_with_headers(sql_str: str, params: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(sql_str, params)
            result = cursor.fetchall()

            schema = []
            for item in cursor.description:
                schema.append(item[0])

            result_dict = []
            for item in result:
                result_dict.append(dict(zip(schema, item)))
            print(result_dict)

            return result_dict

def insert_any(sql_str: str, params: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.executemany(sql_str, params)
            return

def insert(sql_str: str, params: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(sql_str, params)
            return

def update(sql_str: str, params: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(sql_str, params)
            return

def call_proc(sql_str: str, params: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(sql_str, params)
            result = cursor.fetchall()
            return result

def select(sql_str: str, params: list) -> tuple:
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(sql_str, params)
            result = cursor.fetchall()
            return result

