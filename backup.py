from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user, current_user





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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.app_context().push()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



#login form
class LoginForm(FlaskForm):
    username = StringField("Username :",validators=[DataRequired()])
    password = StringField("Password :",validators=[DataRequired()])
    submit = SubmitField("Submit")


#login
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password")
        else:
            flash("user doesn't exist")

    return render_template("login.html",form=form)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))


#dashboard
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = LoginForm()
    return render_template("dashboard.html",form=form)



#blog post model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title =db.Column(db.String(200))
    content = db.Column(db.String (1000))
    author = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(200))

class PostForm(FlaskForm):
    title = StringField("Title : ",validators=[DataRequired()])
    content = TextAreaField("Content : ",validators=[DataRequired()])
    author = StringField("Author : ",validators=[DataRequired()])
    slug = StringField("Slug : ",validators=[DataRequired()])
    submit = SubmitField("Submit")


    
#create a model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), nullable=False,unique=True)
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
    username = StringField("Username :", validators=[DataRequired()])
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
            user = Users(name = form.name.data,username = form.username.data, email=form.email.data, month=form.month.data)
            user.password = form.password_hash.data
            db.session.add(user)
            db.session.commit()
            
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.month.data = ''
        form.password_hash.data = ''
        flash("Added To The Database Successfully ;)")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,name=name,our_users = our_users)

#edit user
# @app.route("/update_user",methods=['GET', 'POST'])
# def update_user():

    
#post page
@app.route("/add-post", methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content = form.content.data, author = form.author.data, slug = form.slug.data)
        form.title.data=''
        form.content.data=''
        form.author.data=''
        form.slug.data=''
        #add post data to the database 
        db.session.add(post)
        db.session.commit()
        flash("Submitted Successfully")
        
    return render_template('add_post.html',form=form)



 

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.username = request.form["username"]
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
@login_required
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

@app.route('/posts')
@login_required
def posts():
    #grab posts from db
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post)

@app.route('/post/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        
        db.session.add(post)
        db.session.commit()
        
        flash("Form Updated Successfully")
        return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)

@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted successfully ")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("Looks like something wrong try again.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

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
    
#its ookk??

#its okk ig...
#gg
