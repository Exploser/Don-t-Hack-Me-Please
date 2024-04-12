from flask import Flask, render_template, request, redirect, url_for, session, flash
from extensions import db, bcrypt
from models import User, Post

# Application Factory
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blogdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    # Index route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                flash('You were successfully logged in')
                return redirect(url_for('dashboard'))
            else:
                flash('Login Failed')
                return render_template('login.html', error="Invalid credentials")
        else:
            return render_template('login.html')

       # Register route
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            try:
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']

                user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
                if user_exists:
                    flash('Username or Email already exists.')
                    return redirect(url_for('register'))

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                flash('Registration successful!')
                return redirect(url_for('login'))
            except Exception as e:
                flash(str(e))
                return render_template('register.html')
        return render_template('register.html')



    # Dashboard route
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            flash('You are not logged in!')
            return redirect(url_for('login'))
        # Here you could retrieve and display user-specific or general information
        return render_template('dashboard.html')

    # Admin Route
    @app.route('/admin')
    def admin():
        if 'user_id' not in session:
            flash('You are not logged in!')
            return redirect(url_for('login'))
        # Logic to handle admin page
        users = User.query.all()
        return render_template('admin.html', users=users)

    @app.route('/admin/add_user', methods=['POST'])
    def add_user():
        if 'user_id' not in session:
            flash('You are not logged in!')
            return redirect(url_for('login'))
        # Logic to add a new user
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists.')
            return redirect(url_for('admin'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!')
        return redirect(url_for('admin'))

    @app.route('/admin/remove_user/<int:user_id>', methods=['POST'])
    def remove_user(user_id):
        if 'user_id' not in session:
            flash('You are not logged in!')
            return redirect(url_for('login'))
        # Logic to remove a user with the given user_id
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User removed successfully!')
        return redirect(url_for('admin'))

    return app

# Run the application
if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host = '0.0.0.0', port=5000, debug=True)
