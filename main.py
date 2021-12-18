import telebot
from config import TOKEN
from db_requests import *


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
        add_user(self.chat_id, self.name, self.surname, self.ISU)
        if self.is_teacher:
            add_teacher(self.chat_id)
        else:
            add_student(self.chat_id)



bot = telebot.TeleBot(f'{TOKEN}', parse_mode=False)

registration = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для обучения с элементами геймификаций.")
    user_answer = Question(message.chat.id)
    registration[message.chat.id] = user_answer
    msg = bot.send_message(user_answer.chat_id, 'Зарегистрируйся. Введи свое имя')
    bot.register_next_step_handler(msg, process_registration_name)

def process_registration_name(message):
    user_answer = registration[message.chat.id]
    user_answer.name = message.text
    msg = bot.send_message(user_answer.chat_id, 'Введите фамилию')
    bot.register_next_step_handler(msg, process_registration_surname)

def process_registration_surname(message):
    user_answer = registration[message.chat.id]
    user_answer.surname = message.text
    msg = bot.send_message(user_answer.chat_id, 'Введите ISU номер')
    bot.register_next_step_handler(msg, process_registration_ISU)

def process_registration_ISU(message):
    user_answer = registration[message.chat.id]
    user_answer.ISU = message.text
    msg = bot.send_message(user_answer.chat_id, 'Вы учитель? Да/Нет')
    bot.register_next_step_handler(msg, process_registration_is_teacher)


def process_registration_is_teacher(message):
    user_answer = registration[message.chat.id]
    answer = message.text
    if answer == 'Да':
        user_answer.is_teacher = True
    elif answer == 'Нет':
        user_answer.is_teacher = False
    del registration[user_answer.chat_id]

bot.infinity_polling()

