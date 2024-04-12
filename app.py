from flask import Flask, request, render_template, session, redirect, url_for, flash
from extensions import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

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
        # Example user credentials
        if username == 'admin' and password == 'password':
            session['username'] = username
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
    flash('Registration is disabled.')
    return redirect(url_for('login'))


# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
    # Here you could retrieve and display user-specific or general information
    return render_template('dashboard.html')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
