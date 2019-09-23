import sqlite3, hashlib

conn = sqlite3.connect('r.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userid INTEGER PRIMARY KEY AUTOINCREMENT, 
		email TEXT NOT NULL,
        password TEXT,
		firstname TEXT,
		lastname TEXT,
		phone INTEGER
		)''')
conn.close()