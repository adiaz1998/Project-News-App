from flask import session, render_template, redirect, g, url_for
from flaskext.mysql import MySQL
from user import registerUser, signIn, userProfile, forgotPassword, resetPassword, editProfile, changePassword, getHomePage
from newsfeed import retrieveNewsFeed
from follow import retrieveUsers
from __init__ import app

mysql = MySQL(app)


@app.route('/')
def index():
    if g.user:
        return getHomePage(g.user, mysql)
    return render_template("login-form.html")

@app.route('/login-form.html')
def login_form():
    return render_template("login-form.html")


@app.route('/signup-form.html')
def signup_form():
    return render_template("signup-form.html")


@app.route('/homepage.html')
def homepage():
    if g.user:
        print(" \n\nAWFAFWAFAFWAFDWAFWAFWA \n\n\n\n LAWFAWFA" + str(g.user))
        return getHomePage(g.user, mysql)
        #return render_template("homepage.html")
    return redirect(url_for('index'))


@app.route('/settings.html')
def settings():
    if g.user:
        return render_template("settings.html")
    else:
        print("lol")
        render_template("login-form.html")


@app.route('/edit_password.html')
def edit_password():
    if g.user:
        return render_template("edit_password.html")
    else:
        return render_template("login-form.html")


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/password_reset.html')
def resetpage():
    return render_template("password_reset.html")

@app.route('/users.html')
def usersPage():
    return render_template("users.html")

@app.route("/register", methods=['POST'])
def register():
    return registerUser(mysql)


@app.route("/login", methods=['POST'])
def login():
    return signIn(mysql)


@app.route("/profile/<username>", methods=['GET'])
def user(username):
    if g.user:
        g.user = username
        return userProfile(g.user, mysql)
    return redirect(url_for('index'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    return forgotPassword(mysql)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    return resetPassword(token, mysql)


@app.route('/profile/<username>', methods=['POST'])
def edit_profile(username):
    if g.user:
        g.user = username
        return editProfile(g.user, mysql)
    return redirect(url_for('index'))


@app.route('/password_change', methods=['POST'])
def password_change():
    if g.user:
        return changePassword(g.user, mysql)
    return redirect(url_for('index'))


@app.route("/newsfeed/<username>", methods=['GET'])
def get_newsfeed(username):
    if g.user:
        g.user = username
        return retrieveNewsFeed(username, mysql)
    return redirect(url_for('index'))

@app.route("/users", methods=['GET'])
def get_users():
    return retrieveUsers(mysql)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
