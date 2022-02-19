#!/usr/bin/env python

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import telebot

from app.cts import get_arrivals, get_stops

logger = telebot.logger
logger.setLevel(logging.INFO)


BASE_DIR = os.getenv("MUX_BASE_DIR")
BASE_URL = os.getenv("MUX_BASE_URL")
BOT_TOKEN = os.getenv("MUX_BOT_TOKEN")
try:
    ALLOWED_USERS = os.getenv("MUX_ALLOWED_USERS").split(',')
except AttributeError:
    print("Missing MUX_ALLOWED_USERS variable")
    sys.exit(1)


bot = telebot.TeleBot(BOT_TOKEN)


def receive_file(message: telebot.types.Message):
    if message.from_user.username not in ALLOWED_USERS:
        bot.reply_to(message, "Not allowed")
        return
    file_info = bot.get_file(message.document.file_id)
    logger.info(f"Got document: {file_info.file_path}")
    _, ext = file_info.file_path.rsplit(".", 1)
    unique_id = file_info.file_unique_id
    file_path = unique_id + "." + ext
    path = Path(BASE_DIR) / file_path
    with open(path, 'wb') as f:
        download = bot.download_file(file_info.file_path)
        f.write(download)

    bot.reply_to(message, BASE_URL + unique_id + "." + ext)


def trams(message: telebot.types.Message):
    longitude = message.location.longitude
    latitude = message.location.latitude

    stops = get_stops(latitude=latitude, longitude=longitude)
    refs = []
    for stop, stop_refs in stops.items():
        refs.extend(stop_refs)
        print(stop, stop_refs)
    arrivals = get_arrivals(refs)
    arrivals_message = []
    for arrival in arrivals:
        eta = datetime.now() - datetime.fromisoformat(arrival['time'])
        arrivals_message.append(f"{arrival['stop']}: {arrival['line']} - {arrival['destination']} - {eta}")
    bot.reply_to(message, '\n'.join(arrivals_message))


def main():
    bot.add_message_handler({
        'function': receive_file,
        'pass_bot': False,
        'filters': {
            'content_types': ["document"],
        },
    })
    bot.add_message_handler({
        'function': trams,
        'pass_bot': False,
        'filters': {
            'content_types': ["location"],
        },
    })
    bot.infinity_polling()


if __name__ == '__main__':
    main()
