from flask import Flask, request, render_template, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3


app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Text, default='user')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

# Vulnerable: SQL Injection possibility in login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            # Convert the row to a dictionary to easily access columns by name
            user = dict(zip([column[0] for column in cursor.description], result))
            if user and user['role'] == 'admin':  # Check if user is not None and then check role
                session['is_admin'] = True
                return redirect(url_for('dashboard'))
            elif user:
                session['is_admin'] = False
                return redirect(url_for('dashboard'))
            else:
                return 'Failure to login! User not found.'
        else:
            return 'Failure to login!'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Fetch all posts from the database
    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/remove_user', methods=['POST'])
def remove_user():
    username = request.form['username']
    user_to_delete = User.query.filter_by(username=username).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return "User not found", 404

@app.route('/update_role', methods=['POST'])
def update_role():
    username = request.form['username']
    new_role = request.form['role']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE user SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
    return redirect('/admin.html')

@app.route('/admin')
def admin():
    users = User.query.all()
    print(users)  # This should output user objects if there are any in the database
    return render_template('admin.html', users=users)



@app.route('/blog')
def blog():
    # Insecurely displaying all posts, assuming they are public
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['blog_title']
    content = request.form['blog_content']
    if title and content:  # Minimal check, still vulnerable
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
        if not User.query.first():  # Adding a default user if empty (for demonstration)
            user = User(username="admin", password="admin")
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)