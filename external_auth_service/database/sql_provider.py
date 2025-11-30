import os

class SQLProvider():
    def __init__(self, file_path):      #file_path - имя(путь) директории где лежат файлы
        self.scripts = {}
        for file in os.listdir(file_path):      #цикл по всем файлам по входной директории
            _sql = open(f'{file_path}/{file}').read()
            self.scripts[file] = _sql

    def get(self, file):
        _sql = self.scripts[file]
        return _sql

