from pyrogram import Client
from configparser import ConfigParser
import time

config = ConfigParser()
config.read('config.ini')

app = Client(
    "my_account",
    config['pyrogram']['api_id'],
    config['pyrogram']['api_hash']
)
#######################################################################################

target = "Marxcela"

with app:
    for i in range(500):
        if i%2 == 0:
            app.send_photo(chat_id=target, photo="./pic.png", caption=f"Mensaje #{i+1} out of 200")
        else:
            app.send_message(target, f"**Hola, Esperancita!**\nMensaje #{i+1} out of 200")
        time.sleep(0.5)

app.run()

