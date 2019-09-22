import sqlite3, hashlib

conn = sqlite3.connect('rto.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY AUTOINCREMENT, 
		email TEXT,
        password TEXT,
		firstName TEXT,
		lastName TEXT,
		phone TEXT
		)''')
conn.close()