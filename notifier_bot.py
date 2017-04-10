import praw
import config
import sys
import time

def bot_login():
    print("Logging in ...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Lanseuo's Weather Comment Responder v0.1")
    print("Logged in")
    return r

def send_message(r, username, subject, body):
    try:
        r.redditor(username).message(subject, body)
    except praw.exceptions.APIException as e:
        if "USER_DOESNT_EXIST" in e.args[0]:
            print("redditor " + username + " not found, did not send a message.")
            return

    print("Send message to " + username + "!")

def get_usernames(filename):
    try:
        with open(filename, "r") as f:
            usernames = f.read()
            usernames = usernames.split("\n")
    except IOError:
        print("Error: File "+ filename + " was not found in the current direcotry!")
        quit()

    return usernames

if len(sys.argv) != 4:
    print("Usage: notifier_bot.py file \"subject\" \"body\"")
    quit()

filename = sys.argv[1]
subject = sys.argv[2]
body = sys.argv[3]

r = bot_login()
usernames = get_usernames(filename)

for username in usernames:
    send_message(r, username, subject, body)
    time.sleep(5)