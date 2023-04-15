import sqlalchemy.exc
from scripts.db_init import *


def new_user(user_id):
    user = Users(telegram_id=user_id)
    print(session.query(Users).all())  # TODO DEBUG
    session.add(user)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        print('Уже в базе')  # TODO DEBUG


def new_tag(user_id, tag_name):
    u_id = session.query(Users).filter(Users.telegram_id == user_id).first().id
    print(u_id)  # TODO DEBUG
    tag = Tags(user_id=u_id, tag_name=tag_name)
    session.add(tag)
    session.commit()
    print(session.query(Users).all())  # TODO DEBUG


def new_file(file_id, tag_id, type):
    pass
