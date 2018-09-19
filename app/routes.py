from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.course import course_list, term_course_schedule, schedule_by_class_numbers
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, GetForm
from app.models import User, Enroll
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = GetForm()
    enrolls = Enroll.query.filter_by(user_id=int(current_user.id))
    enrolls = schedule_by_class_numbers(enroll.class_number for enroll in enrolls)
    if request.args.get('submit') == 'Find':
        term = request.args.get('term')
        subject = request.args.get('subject')
        if request.args.get('catalog') != '':
            catalog = request.args.get('catalog')
            course = term_course_schedule(term, subject, catalog)
            return render_template('course-schedule.html', title='Course Schedule', course=course)
        courses = course_list(term, subject)
        return render_template('course.html', title='%s — Courses' % term, term=term, courses=courses)
    return render_template('home.html', form=form, enrolls=enrolls)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route ('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit ():
        hashed_password = bcrypt.generate_password_hash (form.password.data).decode ('utf-8')
        user = User (username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add (user)
        db.session.commit ()
        flash ('Your account has been created! You are now able to log in.', 'success')
        return redirect (url_for ('login'))
    return render_template ('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        enroll = Enroll (user_id=int (current_user.id), class_number=form.class_number.data)
        db.session.add (enroll)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        flash('Invalid form submission! Please check inputs.', 'danger')

    enrolls = Enroll.query.filter_by(user_id=int(current_user.id))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, enrolls=enrolls)

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    class_number = request.form.get("class_number")
    enroll = Enroll.query.filter_by(class_number=class_number).first()
    db.session.delete(enroll)
    db.session.commit()
    flash('Class deleted!', 'success')
    return redirect(url_for('account'))
