# teste do funcionamento do módulo e do conector do mysql

from modules import mysql_commands as db

conexão = db.conect_mysql("huan", "huan1821")

cursor = conexão.cursor()

cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

for table in tables:
    print(table[0])

cursor.close()
conexão.close()