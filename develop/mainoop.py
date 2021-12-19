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


class BobBot(telebot.TeleBot):
    def __init__(self):
        super().__init__(f'{TOKEN}', parse_mode=False)
        self.registration = {}

    def welcome(self, message):
        self.send_message(message.chat.id, "Привет! Я бот для обучения с элементами геймификаций.")
        self.registration[message.chat.id] = Question(message.chat.id)
        msg = self.send_message(message.chat.id, 'Зарегистрируйся. Введи свое имя')
        self.register_next_step_handler(msg, self.process_registration_name)

    def process_registration_name(self, message):
        user_data = self.registration[message.chat.id]
        user_answer = clear_argument(message.text)
        if check_name(user_answer):
            user_data.name = user_answer
            msg = self.send_message(user_data.chat_id, 'Введите фамилию')
            self.register_next_step_handler(msg, self.process_registration_surname)
        else:
            msg = self.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
            self.register_next_step_handler(msg, self.process_registration_name)

    def process_registration_surname(self, message):
        user_data = self.registration[message.chat.id]
        user_answer = clear_argument(message.text)
        if check_name(user_answer):
            user_data.surname = user_answer
            msg = self.send_message(user_data.chat_id, 'Введите ИСУ номер')
            self.register_next_step_handler(msg, self.process_registration_ISU)
        else:
            msg = self.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
            self.register_next_step_handler(msg, self.process_registration_surname)

    def process_registration_ISU(self, message):
        user_data = self.registration[message.chat.id]
        user_answer = clear_argument(message.text)
        if check_num(user_answer):
            user_data.ISU = user_answer
            msg = self.send_message(user_data.chat_id, 'Вы учитель? Да/Нет')
            self.register_next_step_handler(msg, self.process_registration_position)
        else:
            msg = self.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
            self.register_next_step_handler(msg, self.process_registration_ISU)

    def process_registration_position(self, message):
        user_data = self.registration[message.chat.id]
        user_answer = clear_argument(message.text)
        if user_answer == "Да":
            user_data.is_teacher = True
            del self.registration[user_data.chat_id]
            return
        elif user_answer == "Нет":
            user_data.is_teacher = False
            del self.registration[user_data.chat_id]
            return
        else:
            msg = self.send_message(user_data.chat_id, 'некорректный ввод: введите еще раз')
            self.register_next_step_handler(msg, self.process_registration_position)


bobtt = BobBot()


@bobtt.message_handler(commands=['start'])
def start(message):
    bobtt.welcome(message)


bobtt.infinity_polling()
