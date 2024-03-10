from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

_token = "xoxb-6769719546245-6785303175073-rpd0N345NLXtLanXQcPj5Wex"


def sendMessage(str):
    client = WebClient(token=_token)
    try:
        response = client.chat_postMessage(
            channel="making-bot",
            text=str
        )
        print("success")
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e)
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'