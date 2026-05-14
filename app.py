from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import Config
from models import database, User, Post
from helper import time_ago, allowed_file, UPLOAD_FOLDER
import os
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000  # Limit upload size to 10MB


# Make available to templates
app.jinja_env.globals.update(time_ago=time_ago)

#Initialize the database with the Flask app
database.init_app(app)

# ==============================================
#       ROUTES
# ==============================================

# ============== LANDING ROUTE =================
@app.route('/') 
def index():
    return render_template('index.html')


# ============== AUTH ROUTES =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        display_name = request.form.get('display-name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')

        if (not display_name and not username and not email and not password and not confirm_password):
            flash("All fields are required", "error")
            return render_template('register.html', 
                                   error_display_name=True,
                                   error_username=True,
                                   error_email=True,
                                   error_password=True,
                                   error_confirm_password=True)

        if not display_name:
            flash("Display name is required", "error")
            return render_template('register.html', 
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_display_name=True)
        
        elif len(display_name) < 3:
            flash("Display name must be at least 3 characters", "error")
            return render_template('register.html', 
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_display_name=True)
        
        if not username:
            flash("Username is required", "error")
            return render_template('register.html', 
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_username=True)
        if not email:
            flash("Email is required!", "error")
            return render_template('register.html', 
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_email=True) 
        
        elif len(username) < 3:
            flash("Username must be at least 3 characters", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_username=True)

        if '@' not in email or '.' not in email:
            flash("Email you entered is Invalid!", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_email=True)
        
        if not password:
            flash("Password is required", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_password=True)

        elif len(password) < 6:
            flash("Password must be at least 6 characters", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_password=True)

        if password != confirm_password:
            flash("Password do not match", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_confirm_password=True)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username is already taken!", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_username=True)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already taken!", "error")
            return render_template('register.html',
                                    display_name=display_name,
                                    username=username, 
                                    email=email,
                                    error_email=True)
        
        user = User(username=username, display_name=display_name, email=email)
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
        return redirect(url_for('feed'))
    
    if request.method == "POST":
        login_input = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        username_or_email = login_input

        if not username_or_email and not password:
            flash("All fields are required", "error")
            return render_template('login.html', 
                                   error_username=True,
                                   error_password=True)
        
        if not username_or_email:
            flash("Username is required", "error")
            return render_template('login.html', username_or_email=login_input,
                                   error_username=True)
        
        if not password:
            flash("Password is required", "error")
            return render_template('login.html', username_or_email=login_input,
                                   error_password=True)

        if '@' in username_or_email and '.' in username_or_email:
            user = User.query.filter_by(email=username_or_email).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['display_name'] = user.display_name
            
            flash(f"Welcome back {user.display_name or user.username}!", "success")
            return redirect(url_for('feed'))
        
        else:
            flash("Invalid username or password", "error")
            return render_template('login.html', username_or_email=login_input,
                                   error_username=True, 
                                   error_password=True)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))


# ============== FEED ROUTES =================
@app.route('/feed')
def feed():
    if not session.get('user_id'):
        flash("Session Expired! Please login", "warning")
        return redirect(url_for('login'))

    posts = Post.query.filter_by(visibility='public').order_by(Post.created_at.desc()).all()

    return render_template('feed.html', posts=posts)
    
@app.route('/trending')
def trending():
    if not session.get('user_id'):
        flash("Session Expired! Please login", "warning")
        return redirect(url_for('login'))
    
    return render_template('trending.html')

# ============== UPLOAD ROUTES =================
@app.route('/upload')
def upload():
    if not session.get('user_id'):
        flash("Session Expired! Please login", "warning")
        return redirect(url_for('login'))
        
    return render_template('upload.html')
    
@app.route('/create_post', methods=['POST'])
def create_post():
    if not session.get('user_id'):
        flash("Session Expired! Please login", "warning")
        return redirect(url_for('login'))
    
    if 'meme_image' not in request.files:
        flash("No image selected", "error")
        return redirect(url_for('upload'))
    
    file = request.files['meme_image']
    
    if not file or not allowed_file(file.filename):
        flash("Invalid file type. Allowed: png, jpg, jpeg, gif, webp", "error")
        return redirect(url_for('upload'))

    caption = request.form.get('caption', '')
    category = request.form.get('category', '')
    visibility = request.form.get('visibility', 'public')
    tags_list = request.form.get('tags', '') or None

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)
    
    new_post = Post(
        image_filename=unique_filename,
        caption=caption,
        category=category,
        visibility=visibility,
        tags=tags_list,
        user_id=session['user_id']
    )

    database.session.add(new_post)
    database.session.commit()
    
    flash('Meme uploaded successfully!', 'success')
    return redirect(url_for('feed'))
    
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not session.get('user_id'):
        flash("Session Expired! Please login", "warning")
        return redirect(url_for('login'))

    post = Post.query.get(post_id)

    if post is None:
        flash("Post not found", "error")
        return redirect(url_for('profile'))

    if post and post.user_id == session['user_id']:
        image_path = os.path.join(UPLOAD_FOLDER, post.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

        database.session.delete(post)
        database.session.commit()
        flash("Post deleted successfully!", "success")
    else:
        flash("Post not found or you don't have permission to delete it", "error")

    return redirect(url_for('profile'))

# ============= PROFILE ROUTES =================
@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    post_count = len(user_posts)


    if not user:
        session.clear()
        flash("Session expired. Please login again", "error")
        return redirect(url_for('login'))

    return render_template('profile.html', bio=user.bio or 'No bio yet', 
                           username=user.username, 
                           display_name=user.display_name,
                           user=user,
                           user_posts=user_posts,
                           post_count=post_count)

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if not session.get('user_id'):
        flash("Session Expired! Please login")
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])

    display_name = request.form.get('display-name', '').strip()
    bio = request.form.get('bio', '').strip()

    changed = False

    if display_name and len(display_name) >= 3:
        if display_name != user.display_name:
            user.display_name = display_name
            session['display_name'] = user.display_name
            changed = True
    
    new_bio = bio if bio else "Your bio here"

    if new_bio != user.bio:
        user.bio = new_bio
        changed = True

    if changed:
        database.session.commit()
        flash("Profile updated successfully!", "success")

    else:
        flash("No changes made to the profile", "info")
        
    return redirect(url_for('profile'))

if __name__ == '__main__':
    with app.app_context():
        database.create_all()  # Create tables if they don't exist
    
    # Needed For Render to Publish Live
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)