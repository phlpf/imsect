import dotenv as de
import os

from slack import WebClient
import slackeventsapi as seapi

import block_creator as bc
import backend_manager as bm

de.load_dotenv()

signing_secret = os.getenv("SIGNING_SECRET")
bot_token = os.getenv("BOT_TKN")

slack_events_adapter = seapi.SlackEventAdapter(signing_secret, "/slack/events")

slack_client = WebClient(bot_token)

database = bm.csv_file("database.csv")

@slack_events_adapter.on("app_mention")
def on_message(event_data):
    message = event_data["event"]
    user_mention = "<@%s>"%message["user"]
    if message.get("subtype") is None:
        channel = message["channel"]
        text = message.get('text')
        splitup = text.split(' ')
        if len(splitup) <= 1:
            print(len(splitup), splitup)
            send_message = bc.create_normal_message("hello " + user_mention + "! mention me with `help` for commands.", channel)
            slack_client.chat_postMessage(**send_message)
            return
        handle_command(splitup[1:], channel)    

@slack_events_adapter.on("message")
def on_message(event_data):
    message = event_data["event"]
    user_mention = "<@%s>"%message["user"]
    if message.get("subtype") is None:
        channel = message["channel"]
        text = message.get('text')
        splitup = text.split(' ')
        handle_command(splitup, channel)   

def handle_command(args, channel): 
    command = args[0]
    print("command: ", command, "\narguements: ", args)
    if command == 'help' or 'help' in args:
        send_message = bc.create_normal_message("IMSect. Inventory Management System.\n\
*Command Format: *`@imsect <command> <parameters>`", channel)
        slack_client.chat_postMessage(**send_message)
    elif command == 'test':
        send_message = bc.create_normal_message("this is a test command for WIP features", channel)
        slack_client.chat_postMessage(**send_message)
    elif command == 'get_all':
        raw_message = ""
        for row in database.contents:
            raw_message += ' *|* '.join(row) + '\n\n'
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
    elif command == 'add':
        # add a new item. for now, assume it's the correct format
        # all datapoints are separated by |
        data_str = ' '.join(args[1:])
        data = data_str.split('|')
        database.add_item(data)
        database.save()
        raw_message = ' *|* '.join(data) + '\n\n'
        raw_message = "Added: \n" + raw_message
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
        

@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)