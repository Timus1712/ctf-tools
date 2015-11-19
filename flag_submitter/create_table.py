import sqlite3

db_connection = sqlite3.connect("flags.db")

cursor = db_connection.cursor()

cursor.execute("CREATE TABLE FLAGS (FLAG varchar(255), TIMESTAMP int)")
cursor.execute("CREATE TABLE USED (FLAG varchar(255), TIMESTAMP int)")

db_connection.commit()
db_connection.close()
