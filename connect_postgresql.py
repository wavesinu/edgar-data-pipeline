import psycopg2
from env2 import settings

pcon = settings.POSTGRESQL_CONFIG


class Databases():
    def __init__(self) -> None:
        self.db = psycopg2.connect(host=pcon['host'], dbname=pcon['db'],
                                   user=pcon['user'], port=pcon['port'], password=pcon['password'])
        print('연결 완료')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()
        print('db 연결 종료')

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def insertDB(self, query):
        try:
            self.cursor.execute(query)
            self.db.commit()
            print('insert 완료')
        except Exception as e:
            print(" insert DB err", e)

    def readDB(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)
            result = (" read DB err", e)

        return result

    def deleteTable(self):
        try:
            self.cursor.execute('drop table table1')
            print('테이블 삭제 완료')
        except Exception as e:
            print("delete table error")
