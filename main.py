import constants as keys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import responses as R

print("Bot started.")

def start_command(update, context):
    update.message.reply_text('Type something random to get started!')

def help_command(update, context):
    update.message.reply_text('Ask Google')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling(5)
    updater.idle()

if __name__ == '__main__':
    main()
