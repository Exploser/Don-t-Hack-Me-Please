import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql', 'w') as f:
    connection.executescript("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );

    INSERT INTO users (username, password) VALUES ('admin', 'password123');
    INSERT INTO users (username, password) VALUES ('user', 'mypassword');
    """)
connection.commit()
connection.close()