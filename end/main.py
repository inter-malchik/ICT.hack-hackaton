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


class Task:
    def __init__(self, chat_id):
        self.user_id = chat_id
        self.question = {'question': None, 'answer': None, 'correct': None, 'test': False}

    def __del__(self):
        print(self.user_id, self.question)
        add_tassk(self.user_id, self.question)


bot = telebot.TeleBot(f'{TOKEN}', parse_mode=False)

registration = {}
tasks = {}

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
        user_answer.is_teacher = Trued
    elif answer == 'Нет':
        user_answer.is_teacher = False
    del registration[user_answer.chat_id]

@bot.message_handler(commands=['newtask'])
def add_task(message):
    bot.send_message(message.chat.id, "Создание задания")
    user_task = Task(message.chat.id)
    tasks[message.chat.id] = user_task
    msg = bot.send_message(user_task.user_id, 'Оно будет тестовым?:')
    bot.register_next_step_handler(msg, process_get_is_test)

def process_get_is_test(message):
    user_task = tasks[message.chat.id]
    answer = message.text
    if answer == 'Да':
        user_task.question['test'] = True
    elif answer == 'Нет':
        pass
    msg = bot.send_message(user_task.user_id, 'Отлично. Введите ваше задание:')
    bot.register_next_step_handler(msg, process_create_question)

def process_create_question(message):
    user_task = tasks[message.chat.id]
    user_task.question['question'] = message.text
    if user_task.question['test']:
        msg = bot.send_message(user_task.user_id, 'Отлично. Задание будет состоять из 4 вариантов ответа (A, B, C, D). Введите соответственно через пробем варианты ответов, которые будут доступны')
        bot.register_next_step_handler(msg, process_get_answers_test)
    else:
        msg = bot.send_message(user_task.user_id, 'Отлично. Введите правильный ответ')
        bot.register_next_step_handler(msg, process_get_correct)

def process_get_answers_test(message):
    user_task = tasks[message.chat.id]
    user_task.question['answer'] = message.text.split()
    msg = bot.send_message(user_task.user_id, 'Отлично. Введите правильный ответ (буквой A, B, C, D)')
    bot.register_next_step_handler(msg, process_get_correct)

def process_get_correct(message):
    user_task = tasks[message.chat.id]
    user_task.question['correct'] = message.text
    bot.send_message(user_task.user_id, 'Вопрос создан!')
    del tasks[message.chat.id]




bot.infinity_polling()

