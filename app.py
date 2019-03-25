import os
import json
import schedule, time

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

# set up timer (assumes Heroku is running this script in a while True)
schedule.every().monday.at("15:07").do(log_reminder)

schedule.run_pending()
time.sleep(60) # wait for a minute

def log_reminder(t):
  msg = 'Reminder to do your weekly logs!'
  send_message(msg)

# respond to being tagged in chat
@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()

  # We don't want to reply to ourselves!
  if data['name'] != 'Log Reminder Beta':
    myname = "@Log Reminder Beta"
    if myname in data['text']:
      msg = '{}, you asked for me? I can\'t currently respond to messages yet.'.format(data['name'])
      # msg = '{}, you sent "{}".'.format(data['name'], data['text'])
      send_message(msg)

  return "ok", 200

#def parse_message(data):
#  # We don't want to reply to ourselves!
#  if data['name'] != 'Log Reminder Beta':
#    msg = '{}, you sent "{}".'.format(data['name'], data['text'])
#    send_message(msg)
#    return msg
#
#  return None

def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()

# "data" dictionary format
#  {
#  "attachments": [],
#  "avatar_url": "http://i.groupme.com/123456789",
#  "created_at": 1302623328,
#  "group_id": "1234567890",
#  "id": "1234567890",
#  "name": "John",
#  "sender_id": "12345",
#  "sender_type": "user",
#  "source_guid": "GUID",
#  "system": false,
#  "text": "Hello world ☃☃",
#  "user_id": "1234567890"
#  }
