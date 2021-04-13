from pyrogram import Client, filters
from configparser import ConfigParser
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions, types

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
# I'm sleeping and someone mesaged me, send an automatic message
# Ignore these isers not to automatically reply if I'm sleeping
ignore_users = [703659857, 1057813911]


@app.on_message(filters.private)
def home(client, message):
    print(message)

    name = message.chat.first_name
    message_id = message.message_id
    user = message.from_user
    text = message.text

    message_from_me(name, user, message_id, text)


def message_from_me(name, user, message_id, text):
    global sleeping, last_sleeping_id, last_awake_id, ignore_users
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
            hideTimestamp(hide = True)

        else:
            sleeping = False
            last_awake_id = message_id
            app.delete_messages("me", last_sleeping_id)
            change_bio("\U0001F1E8\U0001F1F4")  # Colombian flag
            hideTimestamp(hide = False)

    elif sleeping:
        if user.id not in ignore_users:
            ignore_users.append(user.id)
            app.send_message(user.id, f"Hey {name}, I'm sleeping right now. "
            "I'll message you when it's the real me \U0001F609\n\n__Regards, my userbot.__")
        else:
            # TODO Already replied once. Think of what to do next, or nothing...
            pass


def change_bio(bio):
    app.send(
        functions.account.UpdateProfile(
            about = bio
        )
    )


def hideTimestamp(hide):
    hideOrShow = types.InputPrivacyValueDisallowAll() if hide else types.InputPrivacyValueAllowAll()
    app.send(
        functions.account.SetPrivacy(
            key= types.InputPrivacyKeyStatusTimestamp(),
            rules= [
                hideOrShow,
            ]
        )
    )


app.run()
