# SIMPLE CODF TO CREATE DB TABLE

import psycopg2

conn = psycopg2.connect(host='127.0.0.1', dbname='postgres',user='postgres',password='pwd',port=5432)
cursor=conn.cursor()

#Doping EDGAR table if already exists.
cursor.execute("DROP TABLE IF EXISTS EDGAR")

#Creating table as per requirement
sql = "CREATE TABLE EDGAR (CIK TEXT, COMPANY TEXT, ITEM_1 TEXT, ITEM_3 TEXT, ITEM_7A TEXT)"

cursor.execute(sql)
print("Table created successfully........")
conn.commit()

#Closing the connection
conn.close()

