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
check = {}
task_default = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    if s.query(Users).filter(Users.user_id == message.chat.id).first() == None:
        bot.send_message(message.chat.id, "Привет! Я бот для обучения с элементами геймификаций.")
        user_answer = Question(message.chat.id)
        registration[message.chat.id] = user_answer
        msg = bot.send_message(user_answer.chat_id, 'Зарегистрируйся. Введи свое имя')
        bot.register_next_step_handler(msg, process_registration_name)
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы")

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
        msg = bot.send_message(user_task.user_id, 'Отлично. Задание будет состоять из 4 вариантов ответа (A, B, C, D). Введите соответственно через пробел варианты ответов, которые будут доступны')
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

@bot.message_handler(commands='checktask')
def check_task(message):
    if is_student(message.chat.id):
        bot.send_message(message.chat.id, 'Вам недоступна эта команда. Проверять задания могут только преподаватели')
    else:
        task = get_task()
        check[message.chat.id] = task
        if task == None:
            bot.send_message(message.chat.id, 'Нет непроверенных заданий')
        else:
            bot.send_message(message.chat.id, task_output(task))
            msg = bot.send_message(message.chat.id, 'Можно ли одобрить это задание? Да/Нет')
            bot.register_next_step_handler(msg, process_get_teacher_check)

def process_get_teacher_check(message):
    task = check[message.chat.id]
    if message.text == "Да":
        task.check = True
        s.commit()
    elif message.text == 'Нет':
        task.delete()
        s.commit()

@bot.message_handler(commands='default_task')
def give_default_task(message):
    if is_teacher(message.chat.id):
        bot.send_message(message.chat.id, 'Вы учитель')
    else:
        passed_tasks = s.query(Completed_tasks).join(Students).join(Users).filter(Users.user_id == message.chat.id).all()
        tasks_quest = s.query(Tasks).filter(Tasks.check and is_teacher(Tasks.user_id)).all()
        passed_tasks_id = []
        for i in passed_tasks:
            passed_tasks_id.append(i.task_id)
        if len(passed_tasks)>=len(tasks_quest):
            bot.send_message(message.chat.id, 'Нет доступных заданий')
        else:
            for i in tasks_quest:
                if i.question_id not in passed_tasks_id:
                    task_default[message.chat.id] = i
                    msg = bot.send_message(message.chat.id, task_output_student(i))
                    bot.register_next_step_handler(msg, process_get_answer_from_student)
                    break
def process_get_answer_from_student(message):
    task = task_default[message.chat.id]
    if str(task.question['correct']) == message.text:
        bot.send_message(message.chat.id, 'Это правильный ответ!')
    else:
        bot.send_message(message.chat.id, 'Это неправильный ответ!')
    new_completed = Completed_tasks()
    new_completed.student_id = s.query(Students).filter(Students.user_id == message.chat.id).first().student_id
    new_completed.task_id = task.question_id
    s.add(new_completed)
    s.commit()
bot.infinity_polling()

