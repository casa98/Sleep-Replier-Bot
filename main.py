from pyrogram import Client
from configparser import ConfigParser
from pyrogram.handlers import MessageHandler

config = ConfigParser()
config.read('config.ini')

app = Client(
    "my_account",
    config['pyrogram']['api_id'],
    config['pyrogram']['api_hash']

)
#######################################################################################

sleeping = False

def dump(client, message):
    global sleeping
    # print(message)
    # Verify it was a private message:
    if(message["from_user"]["is_contact"] and message["chat"]["id"] > 0):
        username = message["from_user"]["username"]
        text = message["text"]
        # Message myself
        if(username == "casa98" and (text == "Sleeping" or text == "Awake")):
            if text == "Sleeping":
                sleeping = True
            else:
                sleeping = False
            app.send_message(username, f"You're now {text}")
        
        # Send automatic messages if I'm sleeping:
        if sleeping and username != "casa98":
            name = message["chat"]["first_name"]
            app.send_message(username, f"Hey, {name}. I am sleeping, my **userbot** sent this message \U0001F648\U0001F64A")


app.add_handler(MessageHandler(dump))

app.run()

app.run()

