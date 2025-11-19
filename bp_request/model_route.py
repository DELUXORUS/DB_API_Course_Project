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
    # err_message = ""
    # if result:
    #     return  ResultInfo(result=result, status=True, err_message=err_message)
    # else:
    #     err_message = 'Данные не получены'
    #     return ResultInfo(result=result, status=False, err_message=err_message)