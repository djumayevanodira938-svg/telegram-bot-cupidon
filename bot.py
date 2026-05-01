import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello")


telegram_app.add_handler(CommandHandler("start", start))


@app.route("/")
def home():
    return "Bot is running!"


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"


def set_webhook():
    asyncio.run(telegram_app.initialize())
    asyncio.run(telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}"))


# run once when app starts
set_webhook()