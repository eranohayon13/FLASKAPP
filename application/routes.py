# import render_template function from the flask module
from flask import render_template
# import the app object from the ./application/__init__.py
from application import app
from application.models import Posts

from flask import render_template, redirect, url_for
from application import app, db
from application.models import Posts
from application.forms import PostForm

#importingbcrypt,users and registraionForm.
from application import app,db,bcrypt
from application.models import Posts,Users
from application.forms import PostForm,RegistrationForm
#import user loogins and methods from flask logins and forms.py
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import PostForm, RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, request


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            title = form.title.data,
            content = form.content.data
        )

        db.session.add(postData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('post.html', title='Post', form=form)

@app.route('/posts')
def posts():
    allposts = Posts.query.all()
    return render_template('posts.html', posts=allposts)
# define routes for / & /home, this function will be called when these are accessed
@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.first()
    return render_template('home.html', title='Home', post=postData)

@app.route('/about')
def about():
    return render_template('about.html', title='About')
#Code checks to if the user is alreadt logged in,using current_user.is_authenticated.
#If formn is valid it checks if the user entered exists and if their password is correct using bcrypt.
#If correct it logs the user in using login_user and sets remember to true or false, deoneding on whether the 
#box is ticked.
#then there it requests from flask library to define a next page or just go to home page.
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

#create register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = Users(email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
