import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretKey'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer, default=0, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

class Assignments(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(30), nullable=False)
   subject = db.Column(db.String(30), nullable=False)
   grade = db.Column(db.String(10))
   varified = db.Column(db.Boolean, default=False, nullable=False)

class Image(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   ImageName = db.Column(db.String(50), nullable=False)
   AssignmentId = db.Column(db.Integer, db.ForeignKey(Assignments.id), nullable=False)

class UserAccess(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   UserId = db.Column(db.Integer, db.ForeignKey(User.id))
   AssignmentId = db.Column(db.Integer, db.ForeignKey(Assignments.id))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uName']
        user = User.query.filter_by(username=username).first()
        if user != None:
            if request.form['pWord'] != user.password:
                return render_template('login.html')
            else:
                login_user(user)
                return flask.redirect('/')
        return render_template('login.html')
    return render_template('login.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['uName']
        email = request.form['email']
        password = request.form['pWord']
        temp = User(username = username, password = password, email = email)
        user = User.query.filter_by(username=request.form['uName']).first()
        if user != None:
            return render_template('create.html'), 'username already exists'
        else:
            db.session.add(temp)
            db.session.commit()
            user = User.query.filter_by(username=request.form['uName']).first()
            login_user(user)
            return flask.redirect('/')
    return render_template('create.html')

@app.route('/upload')
@login_required
def upload():  
    return render_template('upload.html')

@app.route('/search')
def search():    
    return render_template('search.html')

@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        oldPassword = request.form['oldP']
        if current_user.password != oldPassword:
            return render_template('update.html')
        updatedUser = User.query.filter_by(id=current_user.id).first()
        updatedUser.password = request.form['newP']
        db.session.commit()
        return flask.redirect('/')
    return render_template('update.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

if __name__ == "__main__":
    app.run(debug=True)