import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy import update

SqlAlchemyBase = dec.declarative_base()

__factory = None


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, unique=True, nullable=False)
    isu_id = sa.Column(sa.Integer, unique=True)
    name = sa.Column(sa.String, nullable=False)
    surname = sa.Column(sa.String, nullable=False)


class CurrentSeason(SqlAlchemyBase):
    __tablename__ = 'current_season'

    student_id = sa.Column(sa.Integer, primary_key=True, unique=True, nullable=False)
    points = sa.Column(sa.Integer, default=0)


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    teacher_id = sa.Column(sa.Integer, primary_key=True, unique=True, nullable=False)
    token = sa.Column(sa.Integer, unique=True)


def global_init(db_file):
    global __factory
    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
