"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

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
def validates_user():
    """Adds user to db"""
    email = request.form.get("email")
    password = request.form.get("password")
    # age = request.form.get("age")
    # zipcode = request.form.get("zipcode")

    # is_user_there = User.query.filter(User.email == email).all()

    is_user_there = db.session.query(User).filter(User.email == email).first()

    if is_user_there:
        flash("You're already registered!")
        return redirect("/login")

    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Success! You were registered!")

    return redirect("/")


@app.route("/login")
def log_in():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def verify_credentials():
    """Vaildating credentials in the database"""

    input_email = request.form.get("email")
    input_password = request.form.get("password")

    user = User.query.filter_by(email=input_email, password=input_password).first()

    if user:
        session['user_id'] = user.user_id
        # session['user_email'] = user.email
        # can't put an object in the session! need to change to dict or pull out things we want
        #         >>> a = A()
        # >>> a.__dict__
        # {'c': 2, 'b': 1}
        print(session['user_id'])

        flash("Logged In")

        return redirect("/user_list")

    else:
        flash("Incorrect email and/or password")

        return redirect("/login")


@app.route("/logout")
def logout():
    """logout"""
    del session["user_id"]
    print(session)
    flash("Logout successful")
    return redirect("/")


@app.route("/user_list")
def shows_user_ratings():
    """shows user ratings"""

    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()

    # movie_list = db.session.query(Rating.movie_id, Rating.score).filter(Rating.user_id == 1).all()
    # movie_list = db.session.query(Rating.movie, Rating.score).filter(Rating.user_id == 1).all()

    ratings = Rating.query.options(db.joinedload('movie')).filter(Rating.user_id == 1).all()

    print(ratings)

    user_ratings = []
    for obj in ratings:
        user_ratings.append([obj.movie.title, obj.score])


    # movie_list = [(1, "brown"), (2, "gray"), (3, "red")]
    return render_template("user_list.html", movie_list=user_ratings, user=user)


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
