from flask import Flask, request, jsonify, render_template, Blueprint  
from models import db, Post
from sqlalchemy import or_


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorials.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates the database tables



# Sets home.html to / (root/start page)
@app.route('/')
def index():
    tutorials = Post.query.all()  # Get all tutorials from the database

    return render_template('home.html', tutorials=tutorials)


@app.route('/submitTutorial')
def submit():
    return render_template('submit.html')

# @app.route('/grabTutorial', methods=['GET'])
# def getTutorial():
#     return jsonify()

@app.route('/putTutorial',methods=['POST'])
def putTutorial():
    data = request.json

    tutorialSubject = data.get('tutorialSubject')
    tutorialDescription = data.get('tutorialDescription')
    tutorialLanguage = data.get('tutorialLanguage')
    tutorialUsername = data.get('tutorialUsername')
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


if __name__ == '__main__':
    app.run(debug=True)