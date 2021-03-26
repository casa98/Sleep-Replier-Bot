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
last_sleeping_id = -1
last_awake_id = -1

@app.on_message(filters.private)
def home(client, message):
    print(message)

    name = message.chat.first_name
    message_id = message.message_id
    user = message.from_user
    text = message.text

    message_from_me(name, user, message_id, text)


def message_from_me(name, user, message_id, text):
    global sleeping, last_sleeping_id, last_awake_id
    # Did I message myself? (Saved Messages)
    if(user.username == "casa98" and (text == "Sleeping" or text == "Awake")):
        # Edit the message I sent to myself
        app.edit_message_text(
            chat_id = "me",
            message_id = message_id,
            text = f"You're now **{text}**"
        )
        
        if text == "Sleeping":
            sleeping = True
            last_sleeping_id = message_id
            app.delete_messages("me", last_awake_id)
            change_bio("I'm sleeping now.")
        else:
            sleeping = False
            last_awake_id = message_id
            app.delete_messages("me", last_sleeping_id)
            change_bio("\U0001F1E8\U0001F1F4")  # Colombian flag

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
