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

@slack_events_adapter.on("app_mention")
def on_message(event_data):
    message = event_data["event"]
    print("message recieved: " + message.get("text"))
    if message.get("subtype") is None:
        channel = message["channel"]
        text = message.get('text')
        splitup = text.split(' ')
        if len(splitup) <= 1:
            send_message = bc.create_normal_message("hello! mention me with `help` for commands.", channel)
            slack_client.chat_postMessage(**send_message)
            return
        handle_command(splitup[1], splitup[1:])    

def handle_command(command, args): 
    pass

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)