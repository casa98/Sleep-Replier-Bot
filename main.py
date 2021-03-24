from pyrogram import Client, filters
from configparser import ConfigParser
from pyrogram.handlers import MessageHandler

config = ConfigParser()
config.read('config.ini')

app = Client(
    "my_account",
    config['pyrogram']['api_id'],
    config['pyrogram']['api_hash']
)


sleeping = False

@app.on_message(filters.private)
def dump(client, message):
    global sleeping
    print(message)

    username = message.from_user.username
    text = message.text
    if(username == "casa98" and (text == "Sleeping" or text == "Awake")):
        if text == "Sleeping":
            sleeping = True
        else:
            sleeping = False
        
        # Message myself
        app.send_message(username, f"You're now {text}")
    
    # Send automatic message if I'm sleeping (set here your username).
    if sleeping and username != "casa98":
        name = message.chat.first_name
        app.send_message(username, f"Hey, {name}. I am sleeping, my **userbot** sent this message \U0001F648\U0001F64A")


app.run()
