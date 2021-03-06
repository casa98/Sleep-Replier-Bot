import constant as const

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
ignore_users = [703659857, 1057813911]


# This function will receive only my messages (Saved Messages)
# Here is where I setup my userbot to determine whether I'm sleeping or not
@app.on_message(filters.me)
def my_messages(client, message):
    global sleeping, last_sleeping_id, last_awake_id
    message_id = message.message_id
    # print(message)

    # I'm going to sleep
    if(message.text in const.sleeping):
        sleeping = True
        last_sleeping_id = message_id
        change_bio(const.sleeping_bio)
        hideTimestamp(hide = True)
        edit_my_message("me", message_id, const.current_status.format("**sleeping**"))
        app.delete_messages("me", last_awake_id)

    # I woke up
    if(message.text in const.awake):
        sleeping= False
        last_awake_id = message_id
        change_bio(const.awake_bio)
        hideTimestamp(hide = False)
        edit_my_message("me", message_id, const.current_status.format("**awake**"))
        app.delete_messages("me", last_sleeping_id)

def edit_my_message(chat_id, message_id, text):
    app.edit_message_text(chat_id = chat_id,message_id = message_id,text = text)


# Recieve all private messages except mine (Saved Messages)
@app.on_message(filters.private & ~filters.me & filters.bot)
def home(client, message):
    global sleeping
    
    if sleeping and message.from_user.id not in ignore_users:    # Private message receives
        print(message)

        name = message.chat.first_name
        user = message.from_user
        message_id = message.message_id
        text = message.text

        message_received(name, user, message_id, text)


def message_received(name, user, message_id, text):
    app.send_message(user.id, const.sleeping_message_1.format(name))


def change_bio(bio):
    app.send(
        functions.account.UpdateProfile(
            about = bio
        )
    )



def hideTimestamp(hide):
    # This function will show/hide last seen to everyone 
    hideOrShow = types.InputPrivacyValueDisallowAll() if hide else types.InputPrivacyValueAllowAll()

    # Exclude given users from the exception above
    exludeContacts = types.InputPrivacyValueAllowUsers(
        users = [
            #FIXME Works but I don't really know [access_hash] meaning
            types.InputUser(user_id=1057813911, access_hash=0)
        ]
    )
    app.send(
        functions.account.SetPrivacy(
            key= types.InputPrivacyKeyStatusTimestamp(),
            rules= [
                hideOrShow,
                exludeContacts
            ]
        )
    )


app.run()
