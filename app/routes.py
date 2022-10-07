from flask import render_template,flash,redirect,url_for,request
from app import app,db
from app.forms import LoginForm,RegistrationForm, UploadForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'boris'}

    posts = [
        {
            'author': {'username':'boris'},
            'body': 'Yo yo I\'m a person'
        },
        {
            'author': {'username':'banana'},
            'body': 'Yo yo I\'m not a person i think'
        }
    ]

    return render_template('index.html',title = 'Home',  posts = posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratz you are a new registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author': user,
            'body': 'Test posts #1'
        },
        {
            'author': user,
            'body': 'Test posts #2'
        }
    ]
    return render_template('user.html',user=user,posts=posts)

@app.route('/upload',methods=['GET','POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/'+filename)
        return redirect(url_for('upload'))
    return render_template('upload.html',form=form)
