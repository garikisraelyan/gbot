import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from tools.processers import (
    message_processer, InvalidRequestException
)
from tools.checkers import get_link_type

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

You can also:
    - Send a YouTube video link and I'll send that video back to you!
    - Send an Instagram reel link and I'll send that reel back to you!    
""")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "The bot is working :)"
    )


# Handlers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    logger.info(f"User {update.message.chat.id}: {text}")
    try:
        video_link = message_processer(text)
        if video_link:
            video_link_type = get_link_type(video_link)
            if video_link_type == "Path":
                with open(video_link, 'rb') as file:
                    await update.message.reply_video(
                        video=file, supports_streaming=True
                    )
                os.remove(video_link)
            if video_link_type == "URL":
                await update.message.reply_text(
                    f"Here's your reel:\n{video_link}"
                )
    except InvalidRequestException as e:
        logger.error(e)


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    logger.info("The bot is running...")

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(poll_interval=3)
