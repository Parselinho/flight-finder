from twilio.rest import Client
import os

AUTH_TOKEN = os.environ.get("TAWIL_AUTH_TOKEN")


ACCOUNT_SID = os.environ.get("ACCOUNT_SID")


class NotificationManager:
    def __init__(self) -> None:
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, msg_value):
        message = self.client.messages.create(
            body=msg_value,
            from_="+14243720882",
            to="+972546312947",
        )
        print(message.sid)
