from flask import Flask, render_template, redirect , url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, SuggestForm, ResetForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "MxyXJ7jilWXzJQOmtsNZassjg"

Bootstrap(app) # Connect bootstrap with flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'  # Connect database with flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)  # Connects the app to a login manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# Identify all columns by name and data type
class Cafes(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))
    
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    

# db.create_all()

@app.route("/")  # Renders the homepage
def home():
    return render_template('index.html')


@app.route("/cafes") # Renders the cities page
def cafes():
    cafes = Cafes.query.all()
    amount = len(cafes)
    return render_template('cafes.html', cafes=cafes, amount=amount)

@app.route("/register", methods=["POST", "GET"])
def register(): # This registers users into the site
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            flash("This email has already been registered! Log in instead!")
            return redirect(url_for('login'))
        else:
            new_user = Users(username=form.username.data,
                            email=form.email.data,
                            password=generate_password_hash(form.password.data,
                                                            method="pbkdf2:sha256", 
                                                            salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('login.html', form=form, word='Sign Up')

@app.route("/users/login", methods=["GET", "POST"]) # Renders the login page
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
                else:
                    flash("email or password incorrect!")
            else:
                flash("email or password incorrect!")
        return render_template('login.html', form=form, word="Login")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        return render_template('login.html', word='logout')
    elif request.method =="POST":
        logout_user()
        flash("You have been logged out")
        return redirect(url_for('login'))

@app.route("/<int:id>/<path:name>") # Renders page for a cafe
def cafe(name, id):
    cafe = Cafes.query.get(id)
    print(cafe.img_url)
    
    return render_template('name.html', name=name, cafe=cafe)

@app.route("/suggest", methods=['GET', 'POST']) # Renders the suggest page
def suggest():
    form = SuggestForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to be logged in to suggest cafes")
        else:
            new_cafe = Cafes(name = form.name.data,
                            map_url=form.map_url.data,
                            img_url=form.img_url.data,
                            location=form.location.data,
                            has_sockets=form.has_sockets.data,
                            has_toilet=form.has_toilet.data,
                            has_wifi=form.has_wifi.data,
                            can_take_calls=form.can_take_calls.data,
                            seats=form.seats.data,
                            coffee_price=form.coffee_price.data
                            )
            db.session.add(new_cafe)
            db.session.commit()
            flash("Cafe added successfully")
            return redirect(url_for('cafes'))
    return render_template('suggest.html', form=form)

@app.route('/update/<int:id>', methods=["GET", "POST"]) # This updates a record in the database
def update(id):
    cafe = Cafes.query.get(id)
    form = SuggestForm(name=cafe.name,
                       map_url=cafe.map_url,
                       img_url=cafe.img_url,
                       location=cafe.location,
                       has_sockets=cafe.has_sockets,
                       has_toilet=cafe.has_toilet,
                       has_wifi=cafe.has_wifi,
                       can_take_calls=cafe.can_take_calls,
                       seats=cafe.seats,
                       coffee_price=cafe.coffee_price)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to be logged in to update cafes")
            return redirect(url_for('login'))
        else:
            cafe.name = form.name.data
            cafe.map_url = form.map_url.data
            cafe.img_url = form.img_url.data
            cafe.location = form.location.data
            cafe.has_sockets = form.has_sockets.data
            cafe.has_toilet = form.has_toilet.data
            cafe.has_wifi = form.has_wifi.data
            cafe.can_take_calls = form.can_take_calls.data
            cafe.seats = form.seats.data
            cafe.coffee_price = form.coffee_price.data
            db.session.commit()
            flash("Cafe Updated successfully")
            return redirect(url_for('cafes'))
    return render_template('suggest.html', form=form)

@app.route("/delete/<int:id>", methods=["GET", "POST"])  # This deletes a cafe from the database
def delete(id):
    if not current_user.is_authenticated:
        flash("You need to be logged in to delete a cafe!")
        return redirect(url_for('login'))
    else: 
        cafe = Cafes.query.get(id)
        db.session.delete(cafe)
        db.session.commit()
        flash("Cafe deleted successfully")
        return redirect(url_for('cafes'))

if __name__ == "__main__":
    app.run(debug=True)
