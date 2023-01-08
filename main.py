import os

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

load_dotenv()

TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv('PORT', 5000))
HEROKU_PATH = os.getenv('HEROKU_PATH')


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    text = "Bonjour !\n"
    text += "Bienvenue sur ce super bot qui vous permet de planifier vos envois avec postcard creator !\n"
    tuto_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    text += f"Pour commencer, il faut créer et m'envoyer votre token de connexion à l'API de La Poste. Toutes les " \
            f"infos sont disponibles <a href='{tuto_url}'>ici</a>\n"
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    return


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Contactez @eliorpap ou @sxyBoi pour plus d\'infos !')
    return


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle all messages."""
    await update.message.reply_text("Je n'ai pas compris votre message, essayez /help pour plus d'infos !")
    return


def main() -> None:
    """Start the bot."""
    print("Going live!")

    # Create application
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - process the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print("Bot starting...")
    if os.environ.get('ENV') == 'DEV':
        application.run_polling()
    elif os.environ.get('ENV') == 'PROD':
        application.run_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                webhook_url=HEROKU_PATH)
    return


if __name__ == '__main__':
    main()
