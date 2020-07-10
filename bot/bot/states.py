from bot.utils import main_menu, enter_name, enter_email_phone, enter_city
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
import requests
import os
import re

os.environ['BOT_TOKEN'] = '1277759652:AAEqz7vixRjOPOu6nkO9b5-jKd80jTqhPpU'
os.environ['API_URL'] = 'http://127.0.0.1:8000/'
os.environ['API_TOKEN'] = 'b213fc249d66d3dafb2a1ce3c60733addbda2f28'
API_TOKEN = os.environ.get('API_TOKEN')
User_Link = os.environ.get('API_URL') + 'User/'
headers = {'Authorization': 'token ' + API_TOKEN}
Review_Link = os.environ.get('API_URL') + 'Review/'
EMAIL_OR_PHONE = ''
TYPE = SUBTYPE = 0

AGREEMENT, NAME, PHONE_EMAIL, REVIEW, USER_INPUT = range(5)  # conv_handler states


def agreement(update, context):
    query = update.callback_query
    # enter your name
    if query.data == 'yes':
        enter_name(update, context)
        return NAME
    # ask to share information
    elif query.data == 'no':
        text = 'Чтобы начать работу, вам необходимо дать согласие <a href="http://www.acdamate.com/terms-of-use/">на обработку персональных данных</a>'
        keyboard = [[
            InlineKeyboardButton('✅ Да', callback_data='yes'),
            InlineKeyboardButton('⛔️  Нет', callback_data='no')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup,
                                 parse_mode='Html')


def start(update, context):
    user_id = update['message']['chat']['id']
    username = update['message']['chat']['username']

    request = requests.get(User_Link + str(user_id), headers=headers).json()

    if 'detail' in request:
        data = {
            'telegram_id': user_id,
            'username': username
        }
        requests.post(User_Link, data=data, headers=headers)
        text = 'Добро пожаловать в чат-бот Индилайт 🤖. Вы согласны <a href="http://www.acdamate.com/terms-of-use/">на обработку персональных данных</a>?'
        # ask to share information
        keyboard = [[
            InlineKeyboardButton('✅ Да', callback_data='yes'),
            InlineKeyboardButton('⛔️  Нет', callback_data='no')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Html')
        return AGREEMENT
    # name not entered
    elif request['name'] == '':
        enter_name(update, context)
        return NAME
    # contact not entered yet
    elif request['email'] == '' and request['phone'] == '':
        enter_email_phone(update, context)
        return PHONE_EMAIL
    elif request['city'] == '':
        enter_city(update, context)
        return REVIEW
    else:
        main_menu(update, context)
        return REVIEW


def name(update, context):
    # save name
    fullname = update['message']['text']
    user_id = update['message']['chat']['id']
    data = {
        'name': fullname
    }
    requests.patch(User_Link + str(user_id) + '/', data=data, headers=headers)

    # enter phone or email
    enter_email_phone(update, context)
    return PHONE_EMAIL


def phone_email(update, context):
    global EMAIL_OR_PHONE
    query = update.callback_query
    if query.data == 'phone':
        EMAIL_OR_PHONE = 'PHONE'
        text = 'Напишите свой номер телефона в формате 7********** или нажмите на кнопку "Поделиться"'
        keyboard = [[KeyboardButton('Поделиться номером', request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                 reply_markup=reply_markup)
    elif query.data == 'email':
        EMAIL_OR_PHONE = 'EMAIL'
        text = 'Напишите свой e-mail'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html')


def check_phone_email(update, context):
    user_data = update['message']['text']
    user_id = update['message']['chat']['id']
    # save email or phone
    if update['_effective_message']['contact']:
        data = {
            'phone': update['_effective_message']['contact']['phone_number']
        }
        requests.patch(User_Link + str(user_id) + '/', data=data, headers=headers)
        enter_city(update, context)
        return REVIEW
    elif re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', user_data):
        data = {'email': user_data}
        requests.patch(User_Link + str(user_id) + '/', data=data, headers=headers)
        enter_city(update, context)
        return REVIEW
    elif re.match(r'^((\+7|7|8)+([0-9]){10})$', user_data):
        data = {'phone': user_data}
        requests.patch(User_Link + str(user_id) + '/', data=data, headers=headers)
        enter_city(update, context)
        return REVIEW
    # data entered is incorrect
    else:
        if EMAIL_OR_PHONE == 'EMAIL':
            text = 'Пожалуйста, введите корректный адрес почты'
            reply_markup = ReplyKeyboardRemove()
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                     reply_markup=reply_markup)
        else:
            text = 'Пожалуйста, введите корректный номер телефона'
            reply_markup = ReplyKeyboardRemove()
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                     reply_markup=reply_markup)


def review(update, context):
    # save city
    user_id = update['message']['chat']['id']
    request = requests.get(User_Link + str(user_id), headers=headers).json()

    if request['city'] == '':
        user_city = update['message']['text']
        data = {
            'city': user_city
        }
        requests.patch(User_Link + str(user_id) + '/', data=data, headers=headers)

    main_menu(update, context)
    return REVIEW


def cooperation(update, context):
    text = 'По вопросам сотрудничества, пожалуйста, напишите на почту info@acdamate.com'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html')

    main_menu(update, context)


def user_input(update, context):
    user_id = update['message']['chat']['id']
    text = update['message']['text']

    while '\n' in text:
        text = text.replace('\n', ' ')

    data = {
        'telegram_id': user_id,
        'reviewtype_id': TYPE,
        'reviewsubtype_id': SUBTYPE,
        'text': text
    }
    requests.post(Review_Link, data=data, headers=headers)
    text = 'Спасибо, ваше обращение принято!'
    keyboard = [[InlineKeyboardButton('↩️ Главное меню', callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=reply_markup, parse_mode='Html')

    return USER_INPUT


def subtype(update, context):
    global SUBTYPE
    query = update.callback_query
    SUBTYPE = data = query.data
    reply_markup = ReplyKeyboardRemove()
    text = ''
    # Качество продукции - product_quality
    if data == '2':
        text = 'Продукция Индилайт охлаждается при помощи специального газа, поэтому первые секунды после открытия мясо и упаковка могут пахнуть этим газом. Через пару минут запах полностью исчезает, однако, если у вас этого не произошло, пожалуйста, оставьте сообщение.'
    elif data == '3':
        text = 'Процесс от разделки до полки занимает 8 часов, однако, если вы остались недовольны свежестью нашей продукции, пожалуйста, оставьте сообщение и укажите, в каком магазине была приобретена продукция.'

    # Упаковка - packging
    elif data == '8':
        text = 'Мы находимся в постоянном поиске решений, которые позволят сохранить свежесть и качество продукта. В настоящее время пластиковая газо-вакуумная упаковка маркирована типом 5. Цифрой 7 маркируется только пленка, которая не подлежит переработке.'
    # Сертификаты - certificates
    elif data == '9':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('halal_certificate.jpeg', 'rb'))
        text = 'Вся продукция Индилайт, за исключением купат, соответствует стандартам качества Халяль'
    elif data == '10':
        context.bot.sendDocument(chat_id=update.effective_chat.id, document=open('SanPin_certificate.pdf', 'rb'))
        text = 'Вся продукция Индилайт прошла сертификацию и соответствует требованиям ГОСТ Р ИСО 22000-2019 и ГОСТ Р ИСО 9001-2015'
    # go back to menu
    elif data == 'menu':
        main_menu(update, context)
        return REVIEW

    # send subtype msg
    if text != '':
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                 reply_markup=reply_markup)

    if not data in ['email', 'phone']:
        if text != '':
            text = 'Оставьте сообщение'
            keyboard = [[InlineKeyboardButton('↩️ Главное меню', callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                     reply_markup=reply_markup)
            return USER_INPUT
        else:
            text = 'Оставьте сообщение'
            msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Html',
                                           reply_markup=reply_markup)
            id = msg['message_id']
            context.bot.delete_message(text='hhh', chat_id=update.effective_chat.id, message_id=id)

            keyboard = [[InlineKeyboardButton('↩️ Главное меню', callback_data='menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(text=text, chat_id=update.effective_chat.id, message_id=id,
                                     reply_markup=reply_markup)
            return USER_INPUT


def product_quality(update, context):
    global TYPE
    TYPE = 1
    text = 'Индилайт строго следит за качеством продукции и внимательно слушает своих покупателей. В этом разделе вы можете оставить обратную связь о качестве нашей продукции'
    keyboard = [[
        InlineKeyboardButton('Запах', callback_data='2'),
        InlineKeyboardButton('❄️ Свежесть', callback_data='3')],
        [InlineKeyboardButton('🍗 Кости', callback_data='4')],
        [InlineKeyboardButton('✏️ Оставить обращение', callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


def product_availability(update, context):
    global TYPE
    TYPE = 2
    text = 'Наличие продукции'
    keyboard = [
        [InlineKeyboardButton('🚫 Пропало из ассортимента', callback_data='5')],
        # [InlineKeyboardButton('❓ Где вас найти?', callback_data='6')],
        [InlineKeyboardButton('✏️ Оставить обращение', callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


def packaging(update, context):
    global TYPE
    TYPE = 3
    text = 'Упаковка'
    keyboard = [
        [InlineKeyboardButton('❗️ Повреждение', callback_data='7'),
         InlineKeyboardButton('♻️ Пластик', callback_data='8')],
        [InlineKeyboardButton('✏️ Оставить обращение', callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


def certificates(update, context):
    global TYPE
    TYPE = 4
    text = 'Сертификаты'
    keyboard = [[
        InlineKeyboardButton('Халяль', callback_data='9'),
        InlineKeyboardButton('СанПин', callback_data='10')],
        [InlineKeyboardButton('✏️ Оставить обращение', callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)