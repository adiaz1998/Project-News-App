import hashlib

from flask import request, render_template, session, url_for
from flask_login import login_user, UserMixin
import pymysql
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect


class User(UserMixin):
    def __init__(self, _id, first_name, last_name, username, password, email):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id).encode(encoding='UTF-8', errors='strict')

    def profilePicture(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @classmethod
    def validateIfFieldExist(cls, db, input, field):
        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM users WHERE " + field + " = %s"
        cursor.execute(query, (input,))
        row = cursor.fetchone()
        if row:
            user = cls(*list(row.values()))
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def get_user(cls, db, input, field):
        if input == "user_id":
            input = int(input)
        else:
            input = str(input)

        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM users WHERE " + field + " = %s"
        cursor.execute(query, (input,))
        user = cursor.fetchone()

        connection.close()

        try:
            # A simpler way to map row names to row values in a dictionary
            user = dict(zip(cursor.description, user))
            user = cls(int(user['id']),
                       user['first_name'],
                       user['last_name'],
                       user['username'],
                       user['password'])
        except Exception:
            user = None

        return user


def registerUser(db):
    data = ""
    if request.method == 'POST' and request.form.get("firstName") and request.form.get("lastName") \
            and request.form.get("username") and request.form.get("password") and request.form.get("password2") \
            and request.form.get("email"):
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['username']
        password = sha256_crypt.hash(request.form['password'])
        email = request.form['email']

        if User.validateIfFieldExist(db, username, "username"):
            data = "A user with the username already exists"
            return render_template('signup-form.html', data=data), 400

        if User.validateIfFieldExist(db, email, "email"):
            data = "A user with the email already exists"
            return render_template('signup-form.html', data=data), 400

        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, username, password, email,))
        connection.commit()
        data = "User created successfully!"
        return render_template('signup-form.html', data=data), 201

    elif request.method == 'POST':
        data = "Please fill out the form!"
        return render_template('signup-form.html', data=data), 400

    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('signup-form.html', data=data), 500


def signIn(db):
    if request.method == 'POST' and request.form.get("username") and request.form.get("password"):
        username = request.form['username']
        password = request.form['password']
        user = User.validateIfFieldExist(db, username, "username")
        if user and sha256_crypt.verify(password, user.password):
            session['logged_in'] = True
            session['user'] = request.form['username']
            return redirect(url_for('homepage')), 301
        else:
            msg = "Error. Invalid username or password"
            return render_template("login-form.html", data=msg), 401
    elif request.method == 'POST':
        msg = "Fill out the form!"
        return render_template("login-form.html", data=msg), 400
    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('signup-form.html', data=data), 500


def userProfile(username, db):
    user = User.validateIfFieldExist(db, username, "username")
    return render_template("user-profile.html", user=user)
