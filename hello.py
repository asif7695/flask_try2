from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#create flask instance
app= Flask(__name__)
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#secret key
app.config['SECRET_KEY'] = "nothing is that secret here"

#initialize the db
db = SQLAlchemy(app)

#create a model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #create a string
    def __repr__(self):
        return '<Name %r>' %self.name

#class for a form
class UserForm(FlaskForm):
    name = StringField("Name :", validators=[DataRequired()])
    email = StringField("Email :", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("Type Your Name Here", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')

def index():
    someone = "goku"
    ar = ['a','b','c','d']
    return  render_template("index.html", someone=someone,ar=ar)

@app.route('/user/<name>')
def user(name):
    return  render_template("user.html", username=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route('/home', methods= ['GET','POST'])
def home():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name= form.name.data
        form.name.data = ''
        flash("Submit Successful")
    return render_template("home.html",name=name,form=form)

@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Added To The Database Successfully ;)")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users = our_users)
  


#nothing



if __name__ == '__main__':
    app.run(debug=True)
    
'''
export FLASK_APP=hello.py
flask run


'''