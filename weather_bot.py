#!/usr/bin/python3
# bot.py

import praw
import config
import time
import os
import requests

def bot_login():
    print("Logging in ...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Lanseuo's Weather Comment Responder v0.1")
    print("Logged in")
    return r

def run_bot(r, comments_replied_to):
    print("Obtaining 25 comments ...")
    for comment in r.subreddit("test").comments(limit=25):
        if "!weather" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print("String with \"!weather\" found found in comment " + comment.id)

            print("Comment: " + comment.body)
            place = comment.body[9:] # get place by removing !weather

            if len(place) == 0: # if no city is given
                reply = "No city given!\n\nUsage: *!weather Stuttgart*"
            else:
                # get weather data from openweathermap
                api_key = config.openweathermap_api_key
                weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + place + "&APPID=" + api_key + "&units=metric").json()["main"]["temp"]
                weather = int(weather)

                reply = "The temperature in " + place + " is " + str(weather) + "°C\n\n*Source: [OpenWeatherMap](https://openweathermap.org)*"
            comment.reply(reply)
            print("Replied to comment " + comment.id + ": "+ reply)

            comments_replied_to.append(comment.id)
            print(comments_replied_to)
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
    print("Sleeping for 10 seconds ...")
    time.sleep(10)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            # comments_replied_to = filter(None, comments_replied_to)
    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()

while True:
    run_bot(r, comments_replied_to)