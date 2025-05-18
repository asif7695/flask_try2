from flask import Flask, render_template, flash, request 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash


#create flask instance
app= Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  #sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:MyStrongPass123!@localhost/our_users'  #mysql 'mysql://username:password@localhost/db_name'

#secret key
app.config['SECRET_KEY'] = "nothing is that secret here"

#initialize the db
db = SQLAlchemy(app)
migrate = Migrate(app,db) #flask --app hello db init

#create a model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False, unique=True)
    month = db.Column(db.String(20))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #password stuff
    password_hash = db.Column(db.String(200))
    @property
    def password(self):
        raise AttributeError("Password is not readable.")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    #create a string
    def __repr__(self):
        return '<Name %r>' %self.name

#class for a form
class UserForm(FlaskForm):
    name = StringField("Name :", validators=[DataRequired()])
    email = StringField("Email :", validators=[DataRequired()])
    month = StringField("Birth Month :", validators=[DataRequired()])
    password_hash = PasswordField("Password :", validators=[DataRequired(), EqualTo('password_hash2', message='Password must mach') ] ) 
    password_hash2 = PasswordField("Confirm Password :", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Type Your email Here", validators=[DataRequired()])
    password_hash = PasswordField("Type Your password Here", validators=[DataRequired()])
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
            #hash pass
            #hashed_pw = generate_password_hash(form.password_hash.data)
            user = Users(name = form.name.data, email=form.email.data, month=form.month.data)
            user.password = form.password_hash.data
            db.session.add(user)
            db.session.commit()
            
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.month.data = ''
        form.password_hash.data = ''
        flash("Added To The Database Successfully ;)")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users = our_users)
  

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.month = request.form["month"]

        try: 
            db.session.commit()
            flash("User updated.")
            return render_template("update.html",form=form, name_to_update=name_to_update,id=id)
        except:
            flash("Error!")
            return render_template("update.html",form=form, name_to_update=name_to_update,id=id)
    else:
        return render_template("update.html",form=form, name_to_update=name_to_update,id=id)

@app.route('/test_pw', methods= ['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        # check by email
        pw_to_check = Users.query.filter_by(email=email).first()
        # check pass
        passed = check_password_hash(pw_to_check.password_hash, password)
        
    return render_template("test_pw.html",email=email,form=form, password=password,pw_to_check=pw_to_check,passed=passed)




@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name=None
    form = UserForm()
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted.")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form,name=name,our_users = our_users)

    except:
        flash("Something is wrong.")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form=form,name=name,our_users = our_users)

@app.route('/date')
def current_current_date():
    fav_pizza = {
        "a" : "A",
        "b" : "B",
        "c" : "C"
    }
    return fav_pizza
    #return {"Date" : datetime.today()}



if __name__ == '__main__':
    app.run(debug=True)
    
'''
export FLASK_APP=hello.py
flask run


'''