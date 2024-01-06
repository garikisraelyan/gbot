import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from tools.yt_video_downloader import (
    message_processer, InvalidRequestException
)

load_dotenv()

TOKEN: str = os.getenv("TOKEN")
BOT_USERNAME: str = os.getenv("BOT_USERNAME")


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hi! I can download videos for you. 
For more information send `/help`.""")
    

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""Here are the list of commands you can use:
/help
/test

Or just send a YouTube video link and I'll send that video back to you!""")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This was supposed to test if the bot is working :)"
    )


# Handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f"User {update.message.chat.id}: {text}")

    try:
        file_path = message_processer(text)
        if file_path:
            with open(file_path, 'rb') as file:
                await update.message.reply_video(
                    video=file, supports_streaming=True
                )
            os.remove(file_path)
    except InvalidRequestException as e:
        print(e)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(poll_interval=3)


# TODO: Replace print statements with logger