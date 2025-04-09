from flask import Flask, request, jsonify, flash, render_template, Blueprint, redirect, url_for, g 
from models import db, Post, User
from sqlalchemy import or_
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # Attach it to the app

# Set the login_view to redirect users to the login page if they're not authenticated
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorials.db'  
app.config['SECRET_KEY'] = 'jyeiuysjdhkj hohjdsa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates the database tables

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sets home.html to / (root/start page)
@app.route('/')
def index():
    tutorials = Post.query.all()  # Get all tutorials from the database

    return render_template('home.html', tutorials=tutorials)


@app.route('/submitTutorial')
@login_required
def submit():
    return render_template('submit.html')

# @app.route('/grabTutorial', methods=['GET'])
# def getTutorial():
#     return jsonify()

@app.route('/putTutorial',methods=['POST'])
def putTutorial():

    userInfo = ''

    if current_user.is_authenticated: #GETS THE CURRENT USER ID AND HELPS USE THIS TO POPULATE IN DB
            g.user = current_user.get_id()
            tempUser = User.query.filter_by(id=current_user.get_id()).first()
            userInfo = tempUser.uName

    data = request.json

    tutorialSubject = data.get('tutorialSubject')
    tutorialDescription = data.get('tutorialDescription')
    tutorialLanguage = data.get('tutorialLanguage')
    # tutorialUsername = data.get('tutorialUsername')
    tutorialUsername = userInfo
    tutorialLink = data.get('tutorialLink')



    post = Post(subject = tutorialSubject, 
                userName = tutorialUsername, 
                description = tutorialDescription, 
                language=tutorialLanguage, 
                githubLink = tutorialLink)
    
    db.session.add(post)
    db.session.commit()

    return jsonify(success=True, message="Tutorial added successfully")

@app.route('/test', methods=['GET']) #This is used to check data in db (debug tool)
def test():
    allPosts = []

    postValues = Post.query.all()

    for tutorialPosts in postValues:
        post_data = {
            "id": tutorialPosts.id,
            "subject": tutorialPosts.subject,
            "username": tutorialPosts.userName,
            "description": tutorialPosts.description,
            "language": tutorialPosts.language,
            "githubLink": tutorialPosts.githubLink
        }
    
        allPosts.append(post_data)
  

    return jsonify(allPosts)



@app.route('/tutorial/<int:tutorial_id>')
def tutorial_page(tutorial_id):
    tutorial = Post.query.get_or_404(tutorial_id)  
    
    return render_template('tutorial.html', tutorial=tutorial)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to homepage if already logged in

    message = None
    message_type = None  # to track whether it's a success or error message
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            message = 'Logged in successfully!'
            message_type = 'success'
            login_user(user, remember=True)
            return redirect(url_for('index'))
        elif user is None:
            message = 'Email does not exist.'
            message_type = 'error'
        else:
            message = 'Incorrect password, try again.'
            message_type = 'error'

    return render_template("login.html", user=current_user, message=message, message_type=message_type)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logs the user out
    return redirect(url_for('index'))  # Redirect to the home page



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to homepage if already logged in

    message = None
    message_type = None  # to track whether it's a success or error message
    
    if request.method == 'POST':
        email = request.form.get('email')
        uName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validation
        if User.query.filter_by(email=email).first():
            message = 'Email already in use.'
            message_type = 'error'
        elif len(email) < 4:
            message = 'Email must be greater than 3 characters.'
            message_type = 'error'
        elif len(uName) < 2:
            message = 'First name must be greater than 1 character.'
            message_type = 'error'
        elif password1 != password2:
            message = 'Passwords don\'t match.'
            message_type = 'error'
        elif len(password1) < 7:
            message = 'Password must be at least 7 characters.'
            message_type = 'error'
        else:
            new_user = User(email=email, uName=uName, password=generate_password_hash(password1, method='pbkdf2:sha256'), isAdmin=True)
            db.session.add(new_user)
            db.session.commit()
            message = 'Account created successfully!'
            message_type = 'success'
            login_user(new_user, remember=True)
            
            flash('Created account sucessfully!', category='success') #DOESN"T SHOW TO USER FOR SOME REASON

            return redirect(url_for('index'))  # Redirect to home page

    return render_template("sign-up.html", user=current_user, message=message, message_type=message_type)





if __name__ == '__main__':
    app.run(debug=True)
