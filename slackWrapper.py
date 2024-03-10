from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

_token = os.environ.get("SLACK_OAUTH_TOKEN")


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