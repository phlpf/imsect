"""
    A Module to help with using blocks
"""

# Create a normal message block
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
# UNUSED: Create a message in a code block
def create_code_message(message, channel):
    return {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            '```\n' +
                            message + '\n'
                            + '```\n\n'
                        ),
                    },
                }
            ]
        }

# alternate name
create_monospace_message = create_code_message
