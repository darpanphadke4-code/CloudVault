import sqlite3

conn = sqlite3.connect("cloudvault.db")
cursor = conn.cursor()

cursor.execute("SELECT id, name, email, password FROM users")
rows = cursor.fetchall()

if rows:
    print("Users in database:\n")
    for row in rows:
        print(row)
else:
    print("No users found.")

conn.close()