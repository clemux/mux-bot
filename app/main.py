#!/usr/bin/env python

import logging
import os
from pathlib import Path

import telebot

logger = telebot.logger
logger.setLevel(logging.INFO)

BASE_DIR = os.getenv("MUX_BASE_DIR")
BASE_URL = os.getenv("MUX_BASE_URL")
BOT_TOKEN = os.getenv("MUX_BOT_TOKEN")
ALLOWED_USERS = os.getenv("MUX_ALLOWED_USERS").split(',')


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['document'])
def receive_file(message: telebot.types.Message):
    if message.from_user.username not in ALLOWED_USERS:
        bot.reply_to(message, "Not allowed")
        return
    file_info = bot.get_file(message.document.file_id)
    logger.info(f"Got document: {file_info.file_path}")
    _, ext = file_info.file_path.rsplit(".")
    unique_id = file_info.file_unique_id
    file_path = unique_id + "." + ext
    path = Path(BASE_DIR) / file_path
    with open(path, 'wb') as f:
        download = bot.download_file(file_info.file_path)
        f.write(download)

    bot.reply_to(message, BASE_URL + unique_id + "." + ext)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
