import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()

  send_message("calling parse_message")
  msg = parse_message(data)
  send_message("received this message: {}".format(msg))
  if msg not None:
  # We don't want to reply to ourselves!
#  if data['name'] != 'Log Reminder Beta':
#    msg = '{}, you sent "{}".'.format(data['name'], data['text'])
    send_message(msg)

  return "ok", 200

def parse_message(data):
  send_message("in parse_message method")
  # We don't want to reply to ourselves!
  if data['name'] != 'Log Reminder Beta':
    send_message("message passes name restriction")
    msg = '{}, you sent "{}".'.format(data['name'], data['text'])
    send_message(msg)
    return msg

  return None

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
