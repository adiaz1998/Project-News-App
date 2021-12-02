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
    return jsonify({'data': data}), 200


def followUser(current_user, other_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "INSERT INTO follow VALUES (NULL, %s, %s)"
    cursor.execute(query, (current_user, other_user,))
    connection.commit()
    response = "Successfully followed user!"
    return jsonify({'message': response}), 200


def unfollowUser(current_user, other_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM follow where User = %s and UserFollow = %s"
    cursor.execute(query, (current_user, other_user,))
    connection.commit()
    response = "Successfully unfollowed user!"
    return jsonify({'message': response}), 200


def userFollowerList(current_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT u.first_name, u.last_name, u.username from users u WHERE u.user_id IN (SELECT f.UserFollow FROM follow f WHERE f.User = %s);"
    cursor.execute(query, (current_user))
    followerList = cursor.fetchall()
    connection.close()
    return jsonify({'followers': followerList}), 200
