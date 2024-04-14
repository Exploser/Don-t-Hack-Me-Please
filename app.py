from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.info(f'Registration attempt with username: {username} and password: {password}')
        # Vulnerable SQL handling here
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        connection = db.engine.raw_connection()  # Get a raw connection
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute(sql)  # Execute the SQL query
        result = cursor.fetchone()  # Fetch the first result
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection


        if result:
            return 'Logged in successfully!'
        else:
            return 'Failure to login!'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.info(f'Login attempt with username: {username} and password: {password}')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

