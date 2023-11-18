import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('AUTH_TOKEN'))

def send_password_reset_email(username, email, link):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "CKDTAH7B7JM7HKHJFM2NQJ8YFZR6",
            "data": {
            "user": username,
            "link": link,
            },
        }
    )