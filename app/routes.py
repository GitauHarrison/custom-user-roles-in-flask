from shutil import register_unpack_format
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
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.role == 'teacher':
            return redirect(url_for('dashboard_teacher'))
        if current_user.role == 'student':
            return redirect(url_for('dashboard_student'))
    return render_template('index.html', title='Home')


@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_admin'))
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


@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_teacher'))
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            course=form.course.data,
            role='teacher'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Teacher registered successfully!')
        return redirect(url_for('login'))
    return render_template('register_teacher.html', title='Teacher Registration', form=form)


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_student'))
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            school=form.school.data,
            role='student'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Student registered successfully!')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Student Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
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
        if current_user.role == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.role == 'teacher':
            return redirect(url_for('dashboard_teacher'))
        if current_user.role == 'student':
            return redirect(url_for('dashboard_student'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard/student')
@login_required
def dashboard_student():
    return render_template('user_student.html', title="Student Dashboard")


@app.route('/dashboard/teacher')
@login_required
def dashboard_teacher():
    return render_template('user_teacher.html', title="Teacher Dashboard")


@app.route('/dashboard/admin')
@login_required
def dashboard_admin():
    return render_template('user_admin.html', title="Admin Dashboard")
