"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, connect_to_db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register")
def show_registration_form():
    """Shows registration form"""

    return render_template("registration_form.html")


@app.route("/register", methods=["POST"])
def adds_user_to_db():
    """Adds user to db"""
    email = request.form("email")
    password = request.form("password")
    age = request.form("age")
    zipcode = request.form("zipcode")

    is_user_there = db.session.query(User).filter(User.email=email).all()

    # if email in is_user_there:
    #     fails
    # else:
    #     add to db/make instance of class

# check if email in table already
    # add user to table by instantiating an instance of user class
    # commit to db
    # fash message - success, you may now rate movies
# else return to registration if email is already in db

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
