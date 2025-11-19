from dataclasses import dataclass


@dataclass
class ResultInfo:
    result: tuple
    status: bool
    err_message: str

def model_route(provider, params: list, sql_file: str, sql_file_param: str, operation):
    sql_str_without_param = provider.get(sql_file)
    sql_str = sql_str_without_param.format(sql_file_param=sql_file_param)
    result = operation(sql_str, params)
    return ResultInfo(result, True, '') if result else ResultInfo(result, False, 'Ошибка запроса')

