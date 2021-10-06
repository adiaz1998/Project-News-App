from flask import request, render_template
import pymysql


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
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


def registerUser(db):
    if request.method == 'POST' and request.form.get("firstName") and request.form.get("lastName") \
            and request.form.get("username") and request.form.get("password") and request.form.get("email"):
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if User.validateIfFieldExist(db, username, "username"):
            jsondata = {"message": "A user with the email already exists", "status": 400}
            return render_template('signup-form.html', data=jsondata), 400

        if User.validateIfFieldExist(db, email, "email"):
            jsondata = {"message": "A user with the email already exists", "status": 400}
            return render_template('signup-form.html', data=jsondata), 400

        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, username, password, email,))
        connection.commit()
        jsondata = {"message": "User created successfully.", "status": 201}
        return render_template('signup-form.html', data=jsondata), 201

    elif request.method == 'POST':
        jsondata = {"message": "Please fill out the form.", "status": 400}
        return render_template('signup-form.html', data=jsondata), 400

    else:
        jsondata = {"message": "The server has encountered a situation it does not know how to handle.", "status": "500"}
        return render_template('signup-form.html', data=jsondata), 400
