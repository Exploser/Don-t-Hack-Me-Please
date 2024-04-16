from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable SQL handling here
        sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        connection = db.engine.raw_connection()  # Get a raw connection
        cursor = connection.cursor()  # Create a cursor object
        cursor.execute(sql)  # Execute the SQL query
        result = cursor.fetchone()  # Fetch the first result
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

        if result:
             return redirect(url_for('dashboard'))
        else:
            return 'Failure to login!'
    return render_template('login.html')

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

@app.route('/blog')
def blog():
    # Insecurely displaying all posts, assuming they are public
    sql = "SELECT * FROM post"  # Insecure SQL query with potential for SQL injection if modified
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample blog post if table is empty
        if not Post.query.first():
            post1 = Post(title="Sample Post", content="This is a sample blog post content.")
            db.session.add(post1)
            db.session.commit()
    app.run(debug=True)