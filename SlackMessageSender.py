import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

_token = "xoxb-6769719546245-6785303175073-rpd0N345NLXtLanXQcPj5Wex"

# slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=_token)

try:
    response = client.chat_postMessage(
        channel="making-bot",
        text="Hello from your app! :tada:"
    )
    print("success")
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    print(e)
    assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'