import telebot
from telebot import types
from config import TOKEN
from checkargs import *
from data import db_session
from data.db_session import User
from data.db_session import CurrentSeason
from data.db_session import Teachers

bot = telebot.TeleBot(f'{TOKEN}', parse_mode=False)
db_session.global_init("db/database.db")
registration = {}

class Question:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.name = None
        self.surname = None
        self.ISU = None
        self.is_teacher = None

    def __del__(self):
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == self.chat_id).first():
            user = User()
            user.name = self.name
            user.surname = self.surname
            user.id = self.chat_id
            user.isu_id = self.ISU

            season = CurrentSeason()
            season.student_id = self.chat_id

            db_sess.add(user)
            db_sess.add(season)

            bot.send_message(self.chat_id, 'Вы зарегистрированы.')
            if self.is_teacher:
                teach = Teachers
                teach.teacher_id = self.chat_id
                teach.token = self.ISU
                db_sess.add(teach)
            db_sess.commit()

        else:
            bot.send_message(self.chat_id, 'Вы уже зарегистрированы. (изменения внесены не будут)')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для обучения с элементами геймификаций.")
    registration[message.chat.id] = Question(message.chat.id)
    msg = bot.send_message(message.chat.id, 'Зарегистрируйся. Введи свое имя')
    bot.register_next_step_handler(msg, process_registration_name)


def process_registration_name(message):
    user_data = registration[message.chat.id]
    user_answer = clear_argument(message.text)
    if check_name(user_answer):
        user_data.name = user_answer
        msg = bot.send_message(user_data.chat_id, 'Введите фамилию')
        bot.register_next_step_handler(msg, process_registration_surname)
    else:
        msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
        bot.register_next_step_handler(msg, process_registration_name)


def process_registration_surname(message):
    user_data = registration[message.chat.id]
    user_answer = clear_argument(message.text)
    if check_name(user_answer):
        user_data.surname = user_answer
        msg = bot.send_message(user_data.chat_id, 'Введите ИСУ номер')
        bot.register_next_step_handler(msg, process_registration_ISU)
    else:
        msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
        bot.register_next_step_handler(msg, process_registration_surname)


def process_registration_ISU(message):
    user_data = registration[message.chat.id]
    user_answer = clear_argument(message.text)
    if check_num(user_answer):
        user_data.ISU = user_answer
        msg = bot.send_message(user_data.chat_id, 'Необходима информация о вашем статусе')
        process_registration_position(message)
    else:
        msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
        bot.register_next_step_handler(msg, process_registration_ISU)


def process_registration_position(message):
    user_data = registration[message.chat.id]
    # user_answer = clear_argument(message.text)
    mark_inline = types.InlineKeyboardMarkup()
    but_yes = types.InlineKeyboardButton(text='Да', callback_data='Да')
    but_no = types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    mark_inline.add(but_yes, but_no)
    bot.send_message(user_data.chat_id, "Вы учитель?", reply_markup=mark_inline)

    # if user_answer == "Да":
    #     user_data.is_teacher = True
    #     del registration[user_data.chat_id]
    #     return
    # elif user_answer == "Нет":
    #     user_data.is_teacher = False
    #     del registration[user_data.chat_id]
    #     return
    # else:
    #     msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
    #     bot.register_next_step_handler(msg, process_registration_position)


@bot.callback_query_handler(func=lambda call: call.message.chat.id in registration.keys())
def callback(call):
    user_data = registration[call.message.chat.id]
    #bot.answer_callback_query(callback_query_id=call.id)
    if call.data == 'Да':
        user_data.is_teacher = True
        del registration[user_data.chat_id]
    elif call.data == "Нет":
        user_data.is_teacher = False
        del registration[user_data.chat_id]
    bot.answer_callback_query(callback_query_id=call.id)

bot.infinity_polling()
