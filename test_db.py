import pymysql
from env import settings

DATABASE_CONFIG = settings.DATABASE_CONFIG

connection = pymysql.connect(
    host=DATABASE_CONFIG['host'], user=DATABASE_CONFIG['user'], password=DATABASE_CONFIG['password'], db=DATABASE_CONFIG['db'])
cursor = connection.cursor()

query = "select product_service_new from table1 where company_cik=320193"

cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.commit()
connection.close()
