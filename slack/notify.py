import os

import requests

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
SLACK_MESSAGE = os.environ.get("SLACK_MESSAGE")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

requests.post(SLACK_WEBHOOK, json={
    "username": "Github Actions",
    "icon_url": "https://avatars1.githubusercontent.com/u/44036562?s=280&v=4",
    "channel": SLACK_CHANNEL,
    "text": SLACK_MESSAGE
})
