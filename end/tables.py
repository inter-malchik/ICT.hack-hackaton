from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://anton:2813@localhost/hack_bot', echo=True)

db = declarative_base()

class Users(db):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    surname = Column(String)
    ISU_id = Column(Integer)
    Tasks = relationship('Tasks')
    Teachers = relationship('Teachers')
    Students = relationship('Students')

class Teachers(db):
    __tablename__ = "Teachers"

    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    token = Column(Integer)
    Users = relationship('Users')

class Tasks(db):
    __tablename__ = "Tasks"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    question = Column(JSON)
    hard_id = Column(Integer, ForeignKey("Hard_table.hard_id"))
    check = Column(Boolean)
    Users = relationship('Users')
    Hard_table = relationship('Hard_table')

class Students(db):
    __tablename__ = 'Students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    rang = Column(Integer)
    money = Column(Integer)
    Users = relationship('Users')

class Current_season(db):
    __tablename__ = 'Current_Season'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'))
    points = Column(Integer)
    Students = relationship('Students')

class Hard_table(db):
    __tablename__ = 'Hard_table'

    hard_id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String)
    points = Column(Integer)
    Students = relationship('Tasks')

db.metadata.create_all(engine)

