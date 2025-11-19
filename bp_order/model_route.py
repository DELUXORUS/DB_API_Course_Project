from dataclasses import dataclass
from flask import current_app
from cache.wrapper import fetch_from_cache


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str

def model_route(provider, params: list, sql_file: str, operation):
    sql_str = provider.get(sql_file)
    result = operation(sql_str, params)
    return ResultInfo(result, True, '') if result else ResultInfo(result, False, 'Ошибка запроса')

def model_route_cache(provider, params: list, sql_file: str, operation):
    sql_str = provider.get(sql_file)
    decorator = fetch_from_cache(sql_file, current_app.config['cache_config'])
    cache_select_dict = decorator(operation)
    result = cache_select_dict(sql_str, params)
    return ResultInfo(result, True, '') if result else ResultInfo(result, False, 'Ошибка запроса')