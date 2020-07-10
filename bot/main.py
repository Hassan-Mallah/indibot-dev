from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import os
from bot.states import (agreement, start, name, review, cooperation, phone_email,
                        check_phone_email, product_availability, product_quality,
                        packaging, certificates, subtype, user_input)

# Dev: load .env locally
# from dotenv import load_dotenv
# load_dotenv()

AGREEMENT, NAME, PHONE_EMAIL, REVIEW, USER_INPUT = range(5)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        AGREEMENT: [CallbackQueryHandler(agreement)],
        NAME: [MessageHandler(Filters.all, name)],
        PHONE_EMAIL: [
            CallbackQueryHandler(phone_email),
            MessageHandler(Filters.all, check_phone_email)
        ],
        REVIEW: [
            MessageHandler(Filters.regex('^Качество продукции$'), product_quality),
            MessageHandler(Filters.regex('^Наличие продукции$'), product_availability),
            MessageHandler(Filters.regex('^Упаковка$'), packaging),
            MessageHandler(Filters.regex('^Сертификаты$'), certificates),
            MessageHandler(Filters.regex('^Сотрудничество$'), cooperation),
            CallbackQueryHandler(subtype),
            MessageHandler(Filters.all, review)
        ],
        USER_INPUT: [MessageHandler(Filters.all, user_input),
                     CallbackQueryHandler(subtype)],
    },
    fallbacks=[]
)

updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
