import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secretKey'
login_manager = LoginManager(app)
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)



from app import db, User


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user



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
            login_user(user)
            return flask.redirect('/')
        return render_template('login.html')
    return render_template('login.html')




# @app.route('/update/', methods = ['GET', 'POST'])
# @login_required
# def update():
#     if request.method == 'POST':
#         oldPassword = request.form['oldP']
#         if current_user.password != oldPassword:
#             return render_template('update.html')
#         updatedUser = User.query.filter_by(id=current_user.id).first()
#         updatedUser.password = request.form['newP']
#         db.session.commit()
#         return flask.redirect('/')
#     return render_template('update.html')





# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return flask.redirect('/')



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)