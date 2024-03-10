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
    except SlackApiError as e:
        # TODO: better logging
        assert e.response["error"]