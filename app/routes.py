from app import app, db
from flask_login import login_required, current_user, login_user,\
    logout_user
from flask import render_template, url_for, redirect, flash
from app.models import User
from app.forms import AdminRegistrationForm, LoginForm, StudentRegistrationForm,\
    TeacherRegistrationForm


def authenticated_user():
    if current_user.role == 'admin':
        return redirect(url_for('dashboard_admin'))
    if current_user.role == 'teacher':
        return redirect(url_for('dashboard_teacher'))
    if current_user.role == 'student':
        return redirect(url_for('dashboard_student'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home')


@app.route('/register/admin')
def register_admin():
    if current_user.is_authenticated:
        authenticated_user()
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            residence=form.residence.data,
            role='admin'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Admin registered successfully!')
        return redirect(url_for('login'))
    return render_template('register_admin.html', title='Admin Registration', form=form)


@app.route('/register/teacher')
def register_teacher():
    if current_user.is_authenticated:
        authenticated_user()
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            residence=form.residence.data,
            role='teacher'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Teacher registered successfully!')
        return redirect(url_for('login'))
    return render_template('register_teacher.html', title='Teacher Registration', form=form)


@app.route('/register/student')
def register_student():
    if current_user.is_authenticated:
        authenticated_user()
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            residence=form.residence.data,
            role='student'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Student registered successfully!')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Student Registration', form=form)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        authenticated_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash(f'Welcome {user.username}')
        authenticated_user()
    return render_template('login.html', title='Login', form=form)
