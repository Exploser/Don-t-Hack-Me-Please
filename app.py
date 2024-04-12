from flask import Flask, request, render_template_string
import sqlite3  # This line imports the sqlite3 module

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
        <h1>Login</h1>
        <form method="post" action="/login">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''
    return render_template_string(html)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Vulnerable SQL Injection code
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    conn = sqlite3.connect('I:/Projects/Don-t-Hack-Me-Please/database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    

    if result:
        return "Logged in successfully."
    else:
        return "Login failed."

if __name__ == '__main__':
    app.run(debug=True)
