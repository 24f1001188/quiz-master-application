from flask import render_template,request,redirect,url_for,flash,session
from app import app
from models import db,Admin,User,Subject,Chapter,Quiz,Questions,Scores
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from functools import wraps

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_login',methods=['POST'])
def user_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('user_login'))
    
    user=User.query.filter_by(username=username).first()

    if not user:
        flash('The E-mail is not registered.Kindly register before login or login with a registered E-mail')
        return redirect(url_for('user_login'))
    
    if not check_password_hash(user.passhash,password):
        flash('Incorrect password,Try again!')
        return redirect(url_for('user_login'))
    
    session['user_id']=user.id
    flash('Logged in Successfully!!')

    return redirect(url_for('user_dashboard'))

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login',methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('admin_login'))
    
    admin=Admin.query.filter_by(username=username).first()

    if not admin:
        flash('Wrong e-mail for admin login')
        return redirect(url_for('admin_login'))
    
    if not check_password_hash(admin.passhash,password):
        flash('Incorrect password,Try again!')
        return redirect(url_for('admin_login'))
    
    session['admin_id']=admin.id
    flash('Logged in Successfully!!')

    return redirect(url_for('admin_dashboard'))

@app.route('/new_user_registration')
def new_user_registration():
    return render_template('register.html')

@app.route('/set_credentials')
def reg_next_page():
    return render_template('reg_next_page.html')

@app.route('/set_credentials', methods=['POST'])
def reg_next_page_post():
    full_name = request.form.get('full_name')
    qualification = request.form.get('qualification')
    dob = request.form.get('dob')

    if not full_name or not qualification or not dob:
        flash('Filling out all the fields is mandatory!')
        return redirect(url_for('new_user_registration'))

    return render_template('reg_next_page.html', full_name=full_name, qualification=qualification, dob=dob)

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    full_name = request.form.get('full_name')
    qualification = request.form.get('qualification')
    dob_string = request.form.get('dob')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    dob=datetime.strptime(dob_string, '%Y-%m-%d').date()

    if not username or not password or not confirm_password:
        flash('Filling out all the fields is mandatory!')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)

    if password!=confirm_password:
        flash('Passwords do not match!!')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)

    user=User.query.filter_by(username=username).first()
    if user:
        flash('The E-mail is already registered.Try again with a new E-mail or login with the existing email')
        return render_template('reg_next_page.html',full_name=full_name, qualification=qualification, dob=dob)
    
    passhash=generate_password_hash(password)

    New_User=User(username=username,passhash=passhash,Full_Name=full_name,Qualification=qualification,DOB=dob)
    db.session.add(New_User)
    db.session.commit()

    return render_template('reg_finished.html',name=full_name)

#decorators for user and admin authentication
#-------

def user_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'user_id' in session:
            return func(*args,**kwargs)
        else:
            flash('Please Login to continue further!')
            return redirect(url_for('user_login'))
    return inner
    
def admin_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'admin_id' in session:
            return func(*args,**kwargs)
        else:
            flash('Please Login to continue further!')
            return redirect(url_for('admin_login'))
    return inner

#-------

@app.route('/user_dashboard')
@user_auth
def user_dashboard():
        user=User.query.get(session['user_id'])
        return render_template('user_dashboard.html',user=user)

@app.route('/admin_dashboard')
@admin_auth
def admin_dashboard():
        admin=Admin.query.get(session['admin_id'])
        return render_template('admin_dashboard.html',admin=admin)
    
@app.route('/user_logout')
@user_auth
def user_logout():
        session.pop('user_id')
        return render_template('logout.html')
    
@app.route('/admin_logout')
@admin_auth
def admin_logout():
        session.pop('admin_id')
        return render_template('logout.html')
    
@app.route('/change_password_user')
@user_auth
def change_pswd_user():
        return render_template('change_pswd.html')
    
@app.route('/change_password_admin')
@admin_auth
def change_pswd_admin():
        return render_template('change_pswd.html')
    
@app.route('/change_password_user',methods=['POST'])
@user_auth
def change_pswd_user_post():
        curr_password=request.form.get('curr_password')
        new_password=request.form.get('new_password')
        confirm_new_password=request.form.get('confirm_new_password')

        if not curr_password or not new_password:
            flash('Filling out all the fields is mandatory')
            return redirect(url_for('change_pswd_user'))
        
        user=User.query.get(session['user_id'])

        if not check_password_hash(user.passhash,curr_password):
            flash('Incorrect Password')
            return redirect(url_for('change_pswd_user'))
        
        if new_password!=confirm_new_password:
            flash('New password and Confirm new password does not match.Please try again!')
            return redirect(url_for('change_pswd_user'))
        
        new_passhash=generate_password_hash(new_password)
        user.passhash=new_passhash
        db.session.commit()

        flash('Password Updated successfully!!')
        return redirect(url_for('user_dashboard'))
    
@app.route('/change_password_admin',methods=['POST'])
@admin_auth
def change_pswd_admin_post():
        curr_password=request.form.get('curr_password')
        new_password=request.form.get('new_password')
        confirm_new_password=request.form.get('confirm_new_password')

        if not curr_password or not new_password:
            flash('Filling out all the fields is mandatory')
            return redirect(url_for('change_pswd_admin'))
        
        admin=Admin.query.get(session['admin_id'])

        if not check_password_hash(admin.passhash,curr_password):
            flash('Incorrect Password')
            return redirect(url_for('change_pswd_admin'))
        
        if new_password!=confirm_new_password:
            flash('New password and Confirm new password does not match.Please try again!')
            return redirect(url_for('change_pswd_admin'))
        
        new_passhash=generate_password_hash(new_password)
        admin.passhash=new_passhash
        db.session.commit()

        flash('Password Updated successfully!!')
        return redirect(url_for('admin_dashboard'))


