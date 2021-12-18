from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Hard_table, Students, Tasks, Teachers, Users, Current_season

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
    print('ВВВВВ')
    print(ISU)
    print(user_one.ISU_id)
    s.add(user_one)
    s.commit()

def add_student(user_id):
    student_one = Students()

    student_one.user_id = user_id
    student_one.rang = 0
    student_one.money = 100
    s.add(student_one)
    s.commit()


def add_teacher(user_id, token=1234323):
    teacher_one = Teachers()

    teacher_one.user_id = user_id
    teacher_one.token = token
    s.add(teacher_one)
    s.commit()

def status():
    pass

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

id_student = 1018883729
id_teacher = 1982891232
