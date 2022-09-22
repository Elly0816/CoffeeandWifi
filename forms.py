from wtforms import StringField, BooleanField, SubmitField, SelectField, PasswordField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL, Email

# Form for adding new cafes
class SuggestForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map_Url", validators=[URL(), DataRequired()])
    img_url = StringField("Image Url", validators=[URL(), DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets?")
    has_toilet = BooleanField("Has Toilets?")
    has_wifi = BooleanField("Has Wi-Fi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = SelectField("Number of Seats", choices=['0-10', '10-20', '20-30', '30-40', '40-50', '50+'], validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("ADD CAFE !")
    
class RegisterForm(FlaskForm):
    username = StringField("User Name: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[Email(), DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    register = SubmitField("Register Me!")

class LoginForm(FlaskForm):
    email = EmailField("email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    login = SubmitField("LOG ME IN!")

class ResetForm(FlaskForm):
    email = EmailField("email: ", validators=[DataRequired()])
    send = SubmitField("Reset Password")