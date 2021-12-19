from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Hard_table, Students, Tasks, Teachers, Users, Current_season, Completed_tasks

engine = create_engine('postgresql+psycopg2://anton:2813@localhost/hack_bot', echo=True)

session = sessionmaker(bind=engine)
s = session()
hard_data = s.query(Hard_table).first()

if hard_data == None:
    hard_1 = Hard_table()
    hard_1.level = '1'
    hard_1.points = 10
    s.add(hard_1)
    s.commit()

def add_user(chat_id, name, surname, ISU):
    user_one = Users()

    user_one.user_id = chat_id
    user_one.name = name
    user_one.surname = surname
    user_one.ISU_id = ISU
    s.add(user_one)
    s.commit()

def add_student(user_id):
    student_one = Students()

    student_one.user_id = user_id
    student_one.rang = 0
    student_one.money = 100
    s.add(student_one)
    s.commit()
    last = s.query(Students).order_by(Students.student_id.desc()).first().student_id
    member = Current_season()
    member.student_id = last
    member.points = 0
    s.add(member)
    s.commit()

def add_teacher(user_id, token=1234323):
    teacher_one = Teachers()

    teacher_one.user_id = user_id
    teacher_one.token = token
    s.add(teacher_one)
    s.commit()


def create_new_season():
    if s.query(Current_season).first() == None:
        data = s.query(Students.student_id).all()
        send_data = []
        for i in data:
            member = Current_season()
            member.student_id = i[0]
            member.points = 0
            send_data.append(member)
        print(send_data)
        s.add_all(send_data)
        s.commit()

def add_tassk(user_id, question):
    task_one = Tasks()
    print(user_id, question)
    task_one.user_id = user_id
    task_one.question = question
    task_one.hard_id = s.query(Hard_table).first().hard_id
    task_one.check = is_teacher(user_id)
    s.add(task_one)
    s.commit()

def is_teacher(user_id):
    if s.query(Teachers).filter(Teachers.user_id == user_id).first() != None:
        return True
    return False

def is_student(user_id):
    if not is_teacher(user_id):
        return True
    return False

def get_task():
    task = s.query(Tasks).filter(Tasks.check == False).first()
    return task

def task_output(task):
    user = s.query(Users).get(task.user_id)
    if task.question['test']:
        result = f"Задания от {user.name} {user.surname}\n\
{task.question['question']}\n\
A - {task.question['answer'][0]}\n\
B - {task.question['answer'][1]}\n\
C - {task.question['answer'][2]}\n\
D - {task.question['answer'][3]}\n\
Предлагаемый правильный ответ: {task.question['correct']}"
    else:
        result = f"Задания от {user.name} {user.surname}\n\
{task.question['question']}\n\
Предлагаемый правильный ответ: {task.question['correct']}\n\
    "
    return result

def task_output_student(task):
    user = s.query(Users).get(task.user_id)
    if task.question['test']:
        result = f"Задания от студента {user.name} {user.surname}\n\
{task.question['question']}\n\
A - {task.question['answer'][0]}\n\
B - {task.question['answer'][1]}\n\
C - {task.question['answer'][2]}\n\
D - {task.question['answer'][3]}\n"
    else:
        result = f"Задание от  {user.name} {user.surname}\n\
{task.question['question']}\n\
    "
    return result

def information_output(user_id):
    user = s.query(Users).filter(Users.user_id == user_id).first()
    result = ''
    commands = f'Введите любое сообщение, чтобы узнать статус в текущем сезоне\n/newtask - создать новое задание\n'
    if is_teacher(user_id):
        result += f"Вы преподаватель - {user.name} {user.surname}. ИСУ номер: {user.ISU_id} \n"
        commands += f'/checktask - одобрить задания студентов\n'
    else:
        result += f"Вы студент - {user.name} {user.surname}. \nИСУ номер: {user.ISU_id} \n"
        commands += f'/defaulttask - решить обычное задание учителя'
    result += f'Текущий сезон:\n'
    curr_season = s.query(Current_season).all()
    for i in sorted(curr_season, key=lambda x: x.points, reverse=True):
        result += f"{i.Students.Users.name} {i.Students.Users.surname} {i.Students.Users.ISU_id} - {i.points}\n"

    result += commands
    return result


create_new_season()


