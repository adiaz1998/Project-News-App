import login as login
from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_login import login_required, LoginManager, current_user
from flaskext.mysql import MySQL
from user import registerUser, signIn, User, userProfile

app = Flask(__name__)

app.secret_key = 'key'

app.config['MYSQL_DATABASE_HOST'] = 'database-2.c66o8xpkeycc.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'blue0918'
app.config['MYSQL_DATABASE_DB'] = 'SP_login'

mysql = MySQL(app)

login_manager = LoginManager()
login.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(mysql, user_id, "id")


@app.route('/')
def index():
    if g.user:
        return render_template("homepage.html")
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
        return render_template("homepage.html")
    return redirect(url_for('index'))


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


@app.route("/register", methods=['POST'])
def register():
    return registerUser(mysql)


@app.route("/login", methods=['POST'])
def login():
    return signIn(mysql)


@app.route("/user/<username>", methods=['GET'])
def user(username):
    if g.user:
        g.user = username
        return userProfile(g.user, mysql)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=5000, debug=True)
