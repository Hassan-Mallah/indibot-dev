from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove


def main_menu(update, context):
    text = 'Главное меню'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html')
    keyboard = [
        [KeyboardButton('Качество продукции'), KeyboardButton('Наличие продукции')],
        [KeyboardButton('Упаковка'), KeyboardButton('Сертификаты')],
        [KeyboardButton('Сотрудничество')]
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    text = 'Здесь вы можете оставить пожелания и обращения о качестве продукции Индилайт. Выберите раздел'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html', reply_markup=markup)


def enter_name(update, context):
    text = '🖌  Введите ваше Имя и Фамилию'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def enter_email_phone(update, context):
    text = 'Чтобы мы могли с вами связаться, поделитесь своим контактом'
    keyboard = [[
        InlineKeyboardButton('📱  Номер телефона', callback_data='phone'),
        InlineKeyboardButton('📩  E-mail адрес', callback_data='email')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


def enter_city(update, context):
    reply_markup = ReplyKeyboardRemove()
    text = '📍  В каком городе вы покупали нашу продукцию?'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html', reply_markup=reply_markup)