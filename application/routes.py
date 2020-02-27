#importingbcrypt,users and registraionForm.
from application import app, db, bcrypt
from application.models import Posts, Users
#import user loogins and methods from flask logins and forms.py
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template, redirect, url_for, request

# define routes for / & /home, this function will be called when these are accessed
@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.all()
    return render_template('home.html', title='Home', posts=postData)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )

        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))

    else:
        print(form.errors)
    return render_template('post.html', title='Post', form=form)

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
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')
    return render_template('login.html', title='Login', form=form)

#create register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hash_pw
                )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))

    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#If the user is just viewing the page it will go to the second block of code ignoring the form.validate_on_submit(), this is becuase nothing is submitted to it will move on ot the get method, ad will set the form boxes to be equal to the data from the database about the user whihc is stored under current_user.
#If something is being submitted then it will execute the first block of code, if the form is vlaid and passes the checks then the information that is sttored under curent_user will then be updated becuase of the sent form, and will commit this info to the database, so when the user views its info it will be the updated info.
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

#Deleting user, this will log the userout and commit the deletions to the database and the rewdirect them yto teh regiester page allowing them to re register/
@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id
    posts = Posts.query.filter_by(user_id=user)
    for post in posts:
            db.session.delete(post)
    account = Users.query.filter_by(id=user).first()
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))
