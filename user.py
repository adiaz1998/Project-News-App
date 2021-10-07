
from flask import request, render_template, session
import pymysql
from passlib.hash import sha256_crypt


class User:
    def __init__(self, _id, first_name, last_name, username, password, email):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

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


def registerUser(db):
    data = ""
    if request.method == 'POST' and request.form.get("firstName") and request.form.get("lastName") \
            and request.form.get("username") and request.form.get("password") and request.form.get("email"):
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
    msg = ""
    if request.method == 'POST' and request.form.get("username") and request.form.get("password"): #flask utilizes the 'name' property rather than the 'id' property when getting form information
        username = request.form['username']
        password = request.form['password']
        user = User.validateIfFieldExist(db, username, "username")
        if user and sha256_crypt.verify(password,user.password):
            session['logged_in'] = True
            session['username'] = request.form['username']
            msg = "Successfully logged in!"
            return render_template("login-form.html", data=msg), 200
        else:
            msg = "Error. Invalid username or password"
            return render_template("login-form.html", data=msg), 401
    elif request.method == 'POST':
        msg = "Fill out the form!"
        return render_template("login-form.html", data=msg), 400
    else:
        data = "The server has encountered a situation it does not know how to handle."
        return render_template('signup-form.html', data=data), 500