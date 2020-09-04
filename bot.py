import dotenv as de
import os
from slack import WebClient
import time, re
de.load_dotenv()

api_key = os.getenv("API_KEY")
bot_token = os.getenv("BOT_TKN")

slack_web_client = WebClient(bot_token)

message =   {
                "channel": "#general",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                "Bot Is Running\n\n"
                            ),
                        },
                    }
                ]
            }

slack_web_client.chat_postMessage(**message)