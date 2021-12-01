import pymysql
from flask import jsonify, render_template

from user import User


def retrieveUsers(db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT username, first_name, last_name from users"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return jsonify({'data': data})
