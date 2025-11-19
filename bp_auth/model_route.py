from dataclasses import dataclass


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str

def model_route(provider, params: list, sql_file: str, operation):
    sql_str = provider.get(sql_file)
    result = operation(sql_str, params)
    return ResultInfo(result, True, '') if result else ResultInfo(result, False, 'Ошибка запроса')

