import dotenv as de
import os

from slack import WebClient
import slackeventsapi as seapi

import block_creator as bc
de.load_dotenv()

signing_secret = os.getenv("SIGNING_SECRET")
bot_token = os.getenv("BOT_TKN")

slack_events_adapter = seapi.SlackEventAdapter(signing_secret, "/slack/events")

slack_client = WebClient(bot_token)

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print("message recieved:", message.get("text"))
    if message.get("subtype") is None and "hello" in message.get('text'):
        channel = message["channel"]
        print(channel, type(channel))
        send_message = bc.create_normal_message("hello", channel)
        slack_client.chat_postMessage(**send_message)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)
"""
trigger = "hello"

@slack_events_adapter.on("message")
def on_message(event_data):
    print("on_message")
    message = event_data["event"]
    print("message recieved: " + message.get("text"))
    if message.get("subtype") is None and trigger in message.get("text"):
        channel=message.channel
        test_message = "hello!"
        print(channel, "is a", type(channel))
        
        slack_client.api_call("chat.postMessage", channel=channel, text=test_message)

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

print("bot running")
slack_events_adapter.start(port=3000)

"""