import telebot
from config import TOKEN
from checkargs import *


class Question:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.name = None
        self.surname = None
        self.ISU = None
        self.is_teacher = None

    def __del__(self):
        print(self.chat_id)
        print(self.name)
        print(self.surname)
        print(self.ISU)
        print(self.is_teacher)


bot = telebot.TeleBot(f'{TOKEN}', parse_mode=False)

registration = {}


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
        user_data.isu = user_answer
        msg = bot.send_message(user_data.chat_id, 'Вы учитель? Да/Нет')
        bot.register_next_step_handler(msg, process_registration_position)
    else:
        msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
        bot.register_next_step_handler(msg, process_registration_ISU)


def process_registration_position(message):
    user_data = registration[message.chat.id]
    user_answer = clear_argument(message.text)
    if user_answer == "Да":
        user_data.is_teacher = True
        del registration[user_data.chat_id]
        return
    elif user_answer == "Нет":
        user_data.is_teacher = False
        del registration[user_data.chat_id]
        return
    else:
        msg = bot.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
        bot.register_next_step_handler(msg, process_registration_position)


bot.infinity_polling()
