# MAKE SURE
# Updates twice a day
# Need to have this pipeline running in docker
# lol

import json

from flask import jsonify
from requests.api import get
from main import mysql
import pandas as pd
from newsapi import NewsApiClient
import pymysql

# Init
from user import User

newsapi = NewsApiClient(api_key='cc25f61892174ebf82454d80258ad77e')


def getTopHeadLines(cat):
    top_headlines = newsapi.get_top_headlines(  # q='bitcoin',
        category=cat,
        language='en',
        country='us')
    return top_headlines


def getHeadlineProperties(var, cat):
    title = []
    authors = []
    urls = []
    date_time = []
    category = []
    sum = 0

    for item, value in var.items():
        # print(item, value)
        # print(str(item), str(value) + "\n")
        if item == "articles":
            # print(value)
            for i in value:
                sum = sum + 1
                print(sum)
                if sum >= 14:
                    break
                else:
                    # utilize an list to append all the values within the JSON file into a list
                    authors.append(i['author'])
                    urls.append(i['url'])
                    date_time.append(i['publishedAt'])
                    title.append(i['title'])
                    category.append(cat)

                    # if i == "source":
                    #   print('source found')

    return authors, urls, date_time, title, category


properties_business = getHeadlineProperties(getTopHeadLines('business'), 'business')
properties_technology = getHeadlineProperties(getTopHeadLines('technology'), 'technology')
properties_general = getHeadlineProperties(getTopHeadLines('general'), 'general')
properties_health = getHeadlineProperties(getTopHeadLines('health'), 'health')
properties_science = getHeadlineProperties(getTopHeadLines('science'), 'science')
properties_sports = getHeadlineProperties(getTopHeadLines('sports'), 'sports')
properties_entertainment = getHeadlineProperties(getTopHeadLines('entertainment'), 'entertainment')


def getLengthArticles(var):
    for item, value in var.items():
        if item == "totalResults":
            print(value)

            return value


ok = json.dumps(getTopHeadLines('technology'), indent=4)
print(ok)

print("\n\n\n")


# create COLUMNS FOR EACH PROPERTY; EXAMPLE: DATAFRAMES
def convertPropertiesToDF(properties_cat):
    i = 0
    data = {'authors': properties_cat[i], 'urls': properties_cat[i + 1], 'date_time': properties_cat[i + 2],
            'title': properties_cat[i + 3], 'category': properties_cat[i + 4]}

    if data:
        dataFrame = pd.DataFrame(data)
        print("\n")
        return dataFrame
    else:
        print("data not found")

    # print(dataFrame['authors'])
    # print(dataFrame['urls'])


dataFrame_general = convertPropertiesToDF(properties_general)

# print(dataFrame)
print("\n\n\n")

article_preference_dictionary = {

    1: convertPropertiesToDF(properties_business),
    2: convertPropertiesToDF(properties_technology),
    3: convertPropertiesToDF(properties_general),
    4: convertPropertiesToDF(properties_sports),
    5: convertPropertiesToDF(properties_health),
    6: convertPropertiesToDF(properties_science),
    7: convertPropertiesToDF(properties_entertainment)

    # 1 = business
    # 2 = technology
    # 3 = general
    # 4 = sports
    # 5 = health
    # 6 = science
    # 7 = entertainment

}

# get the length of the dictionary
print(len(article_preference_dictionary))

print("TESTING THIS OUT.....................")

# put lines 112-116 into the integration aspect of the code

# for k,v in article_preference_dictionary[4].iterrows():
#   print(v['title'])
#  print(v['date_time'])
# print(v['category'])


print("\n\n")


# def insert_newsfeed_data(db, apikey, repeat_time, title, url, date_time, category, keyword, favorite)

def insert_newsfeed_data(db):
    # FETCH DATA FROM NEWSFEED
    # establishing a connection to the database

    connection = db.connect()

    if connection:
        print("connection made")
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # the cursor is utilized for querying sql databases
        if cursor:
            print("cursor variable found")

            query1 = "TRUNCATE TABLE `newsfeed`"

            cursor.execute(query1)

            for i in range(1, (len(article_preference_dictionary) + 1)):
                for k, v in article_preference_dictionary[i].iterrows():

                    print("\n")
                    print(v['title'])
                    print(v['date_time'])
                    print(v['category'])
                    print(v['urls'])

                    query2 = "INSERT INTO newsfeed VALUES (NULL, %s, %s, %s, %s)"

                    if query2:
                        cursor.execute(query2, (v['title'], v['urls'], v['date_time'], v['category'],))
                        print("imported into database")

                    connection.commit()

                    # for i = 0, i <= 2400000, i+= 2200000 #will run this script twice a day

    elif not connection:
        print("ERROR: connection not made...")


insert_newsfeed_data(mysql)
