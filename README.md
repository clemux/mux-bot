# mux-bot

Telegram bot for saving files sent to it into a directory exposed on a webserver

Usage:

Required environment variables:

```
MUX_BOT_TOKEN=<TELEGRAM BOT TOKEN>
MUX_ALLOWED_USERS=clemux
MUX_BASE_DIR=/data/
MUX_BASE_URL=<PUBLIC URL EXPOSING /data>
```

```
$ mux-bot
```

Then send a file to the bot and it will reply with the public URL.
