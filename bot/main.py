from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import os
from bot.states import agreement, start, name, review, cooperation, phone_email, check_phone_email, product_availability, product_quality, packaging, certificates, subtype, user_input


AGREEMENT, NAME, PHONE_EMAIL, REVIEW, USER_INPUT = range(5)

os.environ['BOT_TOKEN'] = '1277759652:AAEqz7vixRjOPOu6nkO9b5-jKd80jTqhPpU'
os.environ['API_URL'] = 'http://127.0.0.1:8000/'
os.environ['API_TOKEN'] = 'b213fc249d66d3dafb2a1ce3c60733addbda2f28'

# VPN/Socks/HTTP
REQUEST_KWARGS = {
    'proxy_url': 'socks5://localhost:9150',
}

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

updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)  # @inditest_bot
dispatcher = updater.dispatcher
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
