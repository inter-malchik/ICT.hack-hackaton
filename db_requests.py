from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import db, Hard_table, Students, Tasks, Teachers, Users, Current_season

engine = create_engine('postgresql+psycopg2://anton:2813@localhost/hack_bot', echo=True)

session = sessionmaker(bind=engine)
s = session()

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
