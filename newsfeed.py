import pymysql
from flask import jsonify

from user import User


def retrieveNewsFeed(username, db):
    user = User.getUser(db, username, "username")
    preferences = ["business", "entertainment", "general1", "health", "science", "sports", "technology"]
    UserPreference = []
    for preference in preferences:
        if User.getUser(db, 1, preference):
            connection = db.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT nf.title, nf.url, nf.dateandtime, nf.category from newsfeed nf, users u WHERE nf.category = %s and u." + preference + " = 1 and u.user_id = %s"
            print(query)
            print(user.id)
            cursor.execute(query, (preference,user.id,))
            rows = cursor.fetchall()
            print(rows)
            UserPreference.append(rows)
            connection.close()
        elif User.getUser(db, 0, preference):
            pass
    return jsonify(results=UserPreference)
