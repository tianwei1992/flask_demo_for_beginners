from datetime import datetime

from flask import render_template, flash, redirect, url_for, request

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)    # 注意模板路径没有包含templates目录


@app.route('/login', methods=['GET', 'POST'])
def login():
    """只有post且验证成功才是rediret首页，不成功的post和get都是redirect到login页"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():    # if a post request...
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

        # 处理url中的next参数,没有默认为'index'
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':    # netloc为空，表示相对域名，安全
            next_page = url_for('index')

        #  跳转到next指向链接
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)    # 表单是带自__init__参数的
    if form.validate_on_submit():    # post request && validate success...
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':    
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # i.e. post request, but validate fail
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
