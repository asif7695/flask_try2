from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditor,CKEditorField
from flask_wtf.file import FileField


#login form
class LoginForm(FlaskForm):
    username = StringField("Username :",validators=[DataRequired()])
    password = StringField("Password :",validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title : ",validators=[DataRequired()])
    #content = TextAreaField("Content : ",validators=[DataRequired()])
    content = CKEditorField('Content',validators=[DataRequired()]) 
    author = StringField("Author : ")
    slug = StringField("Slug : ",validators=[DataRequired()])
    submit = SubmitField("Submit")


#class for a form
class UserForm(FlaskForm):
    name = StringField("Name :", validators=[DataRequired()])
    username = StringField("Username :", validators=[DataRequired()])
    email = StringField("Email :", validators=[DataRequired()])
    month = StringField("Birth Month :", validators=[DataRequired()])
    about = TextAreaField("About :")
    profile_pic = FileField("Add profile pic")
    password_hash = PasswordField("Password :", validators=[DataRequired(), EqualTo('password_hash2', message='Password must mach') ] ) 
    password_hash2 = PasswordField("Confirm Password :", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Type Your email Here", validators=[DataRequired()])
    password_hash = PasswordField("Type Your password Here", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")




class NamerForm(FlaskForm):
    name = StringField("Type Your Name Here", validators=[DataRequired()])
    submit = SubmitField("Submit")
