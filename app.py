from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import database, User
import os

app = Flask(__name__)

#Database configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('RENDER'):
    # Render uses /tmp for writable storage
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
else:
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Initialize the database with the Flask app
database.init_app(app)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        display_name = request.form.get('display-name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')

        print(f"Display name: '{display_name}'")
        print(f"Length: {len(display_name)}")

        if not display_name:
            flash("Display name is required", "error")
            return redirect(url_for('register'))
        
        if not username:
            flash("Username is required", "error")
            return redirect(url_for('register'))

        if len(display_name) <= 3:
            flash("Display name must be at least 3 characters", "error")
            return redirect(url_for('register'))
        
        if len(username) <= 3:
            flash("Username must be at least 3 characters", "error")
            return redirect(url_for('register'))

        if len(password) <= 6:
            flash("Password must be at least 6 characters", "error")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Password do not match", "error")
            return redirect(url_for('register'))
        
        user = User(username=username, display_name=display_name)
        user.set_password(password)

        database.session.add(user)
        database.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id'  in session:
        flash("You are already logged in", "info")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username:
            flash("Username is required", "error")
            return redirect(url_for('login'))
        
        if not password:
            flash("Password is required", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['display_name'] = user.display_name
            
            flash(f"Welcome back {user.display_name or user.username}!", "success")
            return redirect(url_for('home'))
        
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logout", "info")
    return redirect(url_for('landing'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')



if __name__ == '__main__':
    with app.app_context():
        database.create_all()  # Create tables if they don't exist
        print("Database and User table created successfully!")
    app.run(debug=False)
