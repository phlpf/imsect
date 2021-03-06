# Environment to get tokens
import dotenv as de
import os

# Slack API
from slack import WebClient
import slackeventsapi as seapi

# Personal utils
import block_creator as bc
# Main database 
import backend_manager as bm

# Load tokens into the environment
de.load_dotenv()

# Get tokens
signing_secret = os.getenv("SIGNING_SECRET")
bot_token = os.getenv("BOT_TKN")

# Event API, used for main loop
slack_events_adapter = seapi.SlackEventAdapter(signing_secret, "/slack/events")

# Actual client, used to send messages
slack_client = WebClient(bot_token)

# Database
database = bm.ItemDatabase("database.csv")

# A message was recieved that mentioned us in a channel
@slack_events_adapter.on("app_mention")
def on_mention(event_data):
    # Get data about only the message
    message = event_data["event"]
    # Make the user mention in case we need it
    user_mention = "<@%s>"%message["user"]

    if message.get("subtype") is None:
        # Get the channel the message was in
        channel = message["channel"]
        
        text = message.get('text')
        # Split the message into parts
        splitup = text.split(' ')
        # If we don't have any command, send a default message

        if len(splitup) <= 1:
            print(len(splitup), splitup)
            send_message = bc.create_normal_message("hello " + user_mention + "! mention me with `help` for commands.", channel)
            slack_client.chat_postMessage(**send_message)
            return

        handle_command(splitup[1:], channel, user_mention)    

# A message was recieved through a DM
@slack_events_adapter.on("message")
def on_message(event_data):
    message = event_data["event"]
    user_mention = "<@%s>"%message["user"]

    if message.get("subtype") is None:
        channel = message["channel"]

        text = message.get('text')
        splitup = text.split(' ')

        handle_command(splitup, channel, user_mention)   

# Main function
def handle_command(args, channel, mention): 
    # Get the command from the arguements
    command = args[0]
    print("command: ", command, "\narguements: ", args)

    if (command == 'help' or 'help' in args) or (command == 'h' or 'h' in args):
        # Send a message showing how to use the bot
        send_message = bc.create_normal_message("IMSect. Inventory Management System.\n\
*Command Format (in channel): *`@imsect <command> <parameters>`\n\
*Command Format (in dm with bot): *`<command> <parameters>`\n\
_Commands:_\n\
* `help`: this function\n\
* `version`: get the current version of imsect\n\
* `get_all`: list all items in database. it will be very large and have pings, so I recommend you do this in dms\n\
* `add`: add item. syntax for adding item: `add item name|location|in-house number|...`\n\
    - Current valuse you need to supply: Name, Location, In-House Number, Supplier, Type, Project (Optional), Serial Number (Optional)\n\
* `remove <item_index>`: remove an item from the database. use the index of the item to remove it.\n\
* `remove_from <item_index> <amount_to_remove>`: remove an amount of items from a high quantity item (e.g. screws)\n\
* `checkout <item_index>`: take out an item in your name\n\
* `uncheckout <item_index>`: put an item back if you have it\n\
* `search <name_of_item>`: search for a specific items name", channel)

        slack_client.chat_postMessage(**send_message)

    elif command == 'version' or command == 'v':
        send_message = bc.create_normal_message("IMSect. Inventory Management System.\nVersion 1.0.0. Created by `@Philip F.`. Ping him for help.", channel)
        slack_client.chat_postMessage(**send_message)

    elif command == 'get_all':
        # Return a formatted version of the database
        raw_message = database.explanation_row + '\n'
        for i in range(len(database.contents)):
            # If we have one, add a row explaning what the data is
            raw_message += ' *|* '.join(database.contents[i]) + '\n\n'
        
        # Send a message containing all the data
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)

    elif command == 'add':
        # add a new item. for now, assume it's the correct format
        # all datapoints are separated by |
        data_str = ' '.join(args[1:])

        # new lines and commas are used in csv. we can't have them
        if not "\n" in data_str and not ',' in data_str:
            # Format data, add it to the database, and save the database
            data = data_str.split('|')
            saved_item = database.add_item(data)
            database.save()
            
            if saved_item != None:
                # Respond with what we added
                raw_message = ' *|* '.join(saved_item) + '\n\n'
                raw_message = "Added: \n" + raw_message
                send_message = bc.create_normal_message(raw_message, channel)
                
                slack_client.chat_postMessage(**send_message)
            else :
                send_message = bc.create_normal_message("Not enough items!", channel)
                
                slack_client.chat_postMessage(**send_message)
        else:
            # Tell them they can't do that
            raw_message = "Invalid Characters in item. Please do not include commas or new lines in your message"
            send_message = bc.create_normal_message(raw_message, channel)
            
            slack_client.chat_postMessage(**send_message)
    elif command == 'remove':
        if len(args) == 1:
            send_message = bc.create_normal_message("No index provided!", channel)
            slack_client.chat_postMessage(**send_message)
            return
        # Get the index they want to get rid of
        try:
            index = int(args[1])
        except ValueError:
            # Make sure it's actually an index
            send_message = bc.create_normal_message("Need the index of the item you want to remove. To find all indexes, message me `get_all`", channel)
            slack_client.chat_postMessage(**send_message)
            return
        # Actually remove item
        data = database.remove_item(index)
        # If data is None, there was an error. The index was too large
        if data != None:
            # Save the new database
            database.save()
            
            # Tell them what we removed, so they know if it was the right one
            raw_message = ' *|* '.join(data) + '\n\n'
            raw_message = "Removed: \n" + raw_message
            send_message = bc.create_normal_message(raw_message, channel)

            slack_client.chat_postMessage(**send_message)
        else:
            send_message = bc.create_normal_message("Index to large!", channel)
            slack_client.chat_postMessage(**send_message)
    elif command == 'remove_from':
        if len(args) <= 2:
            send_message = bc.create_normal_message("No index provided!", channel)
            slack_client.chat_postMessage(**send_message)
            return
        # Get the index they want to get rid of
        try:
            index = int(args[1])
        except ValueError:
            # Make sure it's actually an index
            send_message = bc.create_normal_message("Need the index of the item you want to remove. To find all indexes, message me `get_all`", channel)
            slack_client.chat_postMessage(**send_message)
            return
        # Get the amount we want to remove
        try:
            amount = int(args[2])
        except ValueError:
            # Make sure it's actually a number
            send_message = bc.create_normal_message("Need the amount you want to remove. To find all amounts, message me `get_all`", channel)
            slack_client.chat_postMessage(**send_message)
            return
        
        data = database.remove_from_item(index, amount)
        if data == None:
            send_message = bc.create_normal_message("Index to large or amount to much!", channel)
            slack_client.chat_postMessage(**send_message)

        # Tell them what we removed, so they know if it was the right one
        raw_message = ' *|* '.join(data) + '\n\n'
        raw_message = "Removed " + str(amount) + " from: \n" + raw_message
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
    
    elif command == "checkout":
        if len(args) == 1:
            send_message = bc.create_normal_message("No index provided!", channel)
            slack_client.chat_postMessage(**send_message)
            return
        user_to_checkout = mention
        # Get the index
        try:
            index = int(args[1])
        except ValueError:
            # Make sure it's actually an index
            send_message = bc.create_normal_message("Need the index of the item you want to remove. To find all indexes, message me `get_all`", channel)
            slack_client.chat_postMessage(**send_message)
            return
        data = database.checkout_item(index, user_to_checkout)
        # Holder is always last property
        if data==None:
            send_message = bc.create_normal_message("Someone else already checked that out (or it doesn't exist)!", channel)
            slack_client.chat_postMessage(**send_message)
            return
            
        # Tell them what we removed, so they know if it was the right one
        raw_message = ' *|* '.join(data) + '\n\n'
        raw_message = "Checkedout: \n" + raw_message
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)

        database.save()
    
    elif command == "uncheckout":
        if len(args) == 1:
            send_message = bc.create_normal_message("No index provided!", channel)
            slack_client.chat_postMessage(**send_message)
            return
        user_to_uncheckout = mention
        # Get the index
        try:
            index = int(args[1])
        except ValueError:
            # Make sure it's actually an index
            send_message = bc.create_normal_message("Need the index of the item you want to remove. To find all indexes, message me `get_all`", channel)
            slack_client.chat_postMessage(**send_message)
            return
        data = database.checkout_item(index, 'N/A', needed_holder=user_to_uncheckout)
        
        # if it didn't work, they probably didn't have it
        if data==None:
            send_message = bc.create_normal_message("You don't have that!", channel)
            slack_client.chat_postMessage(**send_message)
            return
            
        # Tell them what we removed, so they know if it was the right one
        raw_message = ' *|* '.join(data) + '\n\n'
        raw_message = "Uncheckedout: \n" + raw_message
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)

        database.save()
    elif command == "search":
        if len(args)==1:
            send_message = bc.create_normal_message("No search term provided!", channel)
            slack_client.chat_postMessage(**send_message)
            return
        term = args[1]

        matches = database.search_for(term)
        
        # Tell them what we removed, so they know if it was the right one
        raw_message = "Matches: \n\n"
        for m in matches:
            raw_message += ' *|* '.join(m) + '\n\n'
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
    elif command == "update":
        database.read_from_sheet()
        database.save()
        raw_message = "New Database: \n\n"
        for row in database.contents:
            raw_message += ' *|* '.join(row) + '\n\n'
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
    elif command == "revert":
        database.revert()
        database.save()
        raw_message = "Reverted Database: \n\n"
        for row in database.contents:
            raw_message += ' *|* '.join(row) + '\n\n'
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)
    elif command == "save":
        database.save()
        raw_message = "Saved to Google Sheet!\n\n"
        send_message = bc.create_normal_message(raw_message, channel)
        slack_client.chat_postMessage(**send_message)

# Uh oh. An error occured. Log it, but don't stop 
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)