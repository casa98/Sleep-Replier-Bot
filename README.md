# Sleep-Replier-Bot
This **Telegram userbot** will help you automatically reply to private chats when you send **Sleeping** to *Saved Messages*. To revert the action, send **Awake**, which would represent you're now awake and can reply by yourself.

## Installation
Repo contains a `requirements.txt` file which you can use to install required packages in a *virtualenv* or whatever you want.

Main package is [Pyrogram](https://docs.pyrogram.org/) whose documentation is full of examples.

## Authentication
As this is a userbot (not a regular bot like [@GitHubBot](https://t.me/GithubBot)), 
there is an ingored file called `config.ini` in the root repository which is used by the [MTProto API](https://core.telegram.org/mtproto) 
to impersonate your identity, that's why it can reply messages as if it were **you** while you're snoring.

This mentioned file includes a **Telegram API key** (API *id/hash* pair), which you can obtain [here](https://my.telegram.org/auth?to=apps). 
Rememeber to login using your credentials as it will be your own userbot. Once you have these two values, create the `config.ini` file as follows:
```
[pyrogram]
api_id = <your api_id>
api_hash = <your api_hash>
```

## How to run
Easy peasy, just run `python3 main.py` and it'll be listening for all incoming messages from all private chats!


## Contributing
Via PRs from a **feature brach** to **main**. All changes, improvements and new ideas are totally welcome!
