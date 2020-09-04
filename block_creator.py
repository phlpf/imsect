
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
def create_code_message(message, channel):
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

# alternate name
create_monospace_message = create_code_message