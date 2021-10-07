from flask import Flask, render_template
from flaskext.mysql import MySQL
from user import registerUser, signIn

app = Flask(__name__)

app.secret_key = 'key'

app.config['MYSQL_DATABASE_HOST'] = 'database-2.c66o8xpkeycc.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'blue0918'
app.config['MYSQL_DATABASE_DB'] = 'SP_login'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("login-form.html")


@app.route('/login-form.html')
def login_form():
    return render_template("login-form.html")


@app.route('/signup-form.html')
def signup_form():
    return render_template("signup-form.html")


@app.route("/register", methods=['POST'])
def register():
    return registerUser(mysql)


@app.route("/login", methods=['POST'])
def login():
    return signIn(mysql)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
