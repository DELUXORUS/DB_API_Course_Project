from pymysql import connect     #объект соеденения с БД
from pymysql.err import OperationalError

class DBContextManager:
    def __init__(self, db_connect: dict):
        self.conn = None
        self.cursor = None
        self.db_connect = db_connect

    def __enter__(self):
        try:
            self.conn = connect(**self.db_connect)
            self.cursor = self.conn.cursor()
            self.conn.begin()   #в этом месте стартуют транзакции (на будущее)
            return self.cursor
        except OperationalError as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val)
        if self.cursor:     #был ли создан курсор
            if exc_type:    #есть ли ошибка
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True
