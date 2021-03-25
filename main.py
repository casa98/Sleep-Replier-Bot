from pyrogram import Client, filters
from configparser import ConfigParser
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions

config = ConfigParser()
config.read('config.ini')

app = Client(
    "my_account",
    config['pyrogram']['api_id'],
    config['pyrogram']['api_hash']
)


sleeping = False

@app.on_message(filters.private)
def home(client, message):
    print(message)

    name = message.chat.first_name
    message_id = message.message_id
    user = message.from_user
    text = message.text

    message_from_me(name, user, message_id, text)


def message_from_me(name, user, message_id, text):
    global sleeping
    # Did I message myself? (Saved Messages)
    if(user.username == "casa98" and (text == "Sleeping" or text == "Awake")):
        if text == "Sleeping":
            sleeping = True
            change_bio("I'm sleeping now.")
        else:
            sleeping = False
            change_bio("\U0001F1E8\U0001F1F4")  # Colombian flag
        
        # Edit the message I sent to myself
        app.edit_message_text(
            chat_id = "me",
            message_id = message_id,
            text = f"You're now **{text}**"
        )

    else:
        if sleeping:
            app.send_message(user.id, f"Hey, {name}.\nI'm sleeping right now, I'll reply when it's the real me \U0001F648\U0001F64A")


def change_bio(bio):
    app.send(
        functions.account.UpdateProfile(
            about = bio
        )
    )

app.run()
