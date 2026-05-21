import sqlite3

# Connect database
conn = sqlite3.connect('student_result.db')

cursor = conn.cursor()

# Read schema.sql
with open('database/schema.sql', 'r') as f:
    sql_script = f.read()

# Execute SQL script
cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Database created successfully.")