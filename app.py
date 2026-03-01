from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'task_secret_key'

# --- 1. MYSQL CONNECTION ---
# Replace 'your_password' with your actual MySQL root password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yor_mysql_password@localhost/auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 2. FIXED ADMIN CREDENTIALS ---
FIXED_ADMIN_USER = 'admin_name'
FIXED_ADMIN_PW = 'admin_password'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    role = db.Column(db.String(10), default='user')

# --- 3. AUTO-SETUP & REFRESH ADMIN ---
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username=FIXED_ADMIN_USER).first()
    
    if admin and not bcrypt.check_password_hash(admin.password, FIXED_ADMIN_PW):
        db.session.delete(admin)
        db.session.commit()
        admin = None
            
    if not admin:
        hashed_pw = bcrypt.generate_password_hash(FIXED_ADMIN_PW).decode('utf-8')
        new_admin = User(username=FIXED_ADMIN_USER, password=hashed_pw, role='admin')
        db.session.add(new_admin)
        db.session.commit()

# --- 4. ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'user_dashboard'))
        flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # NEW SECURITY LOGIC: Block any attempt to register as an 'admin'
        requested_role = request.form['role']
        
        if requested_role == 'admin':
            flash('Cannot register as an Admin. This role is restricted!')
            return redirect(url_for('register'))

        # Standard User Registration
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=request.form['username'], password=hashed_pw, role='user')
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except:
            flash('User already exists!')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('user_dashboard.html', name=session['username'])

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied!", 403
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('profile.html', name=session['username'], role=session['role'])

@app.route('/delete_user/<int:id>')
def delete_user(id):
    if session.get('role') == 'admin':
        user_to_del = User.query.get(id)
        if user_to_del and user_to_del.username != FIXED_ADMIN_USER:
            db.session.delete(user_to_del)
            db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)