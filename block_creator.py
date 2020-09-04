
def create_normal_message(message, channel):
    return {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            message + '\n\n'
                        ),
                    },
                }
            ]
        }