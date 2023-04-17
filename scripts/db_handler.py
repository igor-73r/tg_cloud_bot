import sqlalchemy.exc

from scripts.db_init import *
from scripts.db_session import create_session


def new_user(user_id):
    session = create_session()
    user = Users(telegram_id=user_id)
    session.add(user)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        print('Уже в базе')
    session.close()


def update_current_tag(user_id, tag_name):
    session = create_session()
    user = session.query(Users).filter(Users.id == user_id).first()
    user.current_tag = tag_name
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()


def get_tag_by_id(tag_id):
    session = create_session()
    tag_name = session.query(Tags.tag_name).filter(Tags.id == tag_id).first()[0]
    session.close()
    return tag_name


def remove_tag_by_name(message, tag_name):
    session = create_session()
    update_current_tag(get_db_user_id(message.chat.id), tag_name=None)
    u_id = get_db_user_id(message.chat.id)
    tag = session.query(Tags).filter(Tags.tag_name == tag_name and Tags.user_id == u_id).first()
    files = tag.files
    for i in files:
        session.delete(i)
    session.delete(tag)
    session.commit()
    session.close()
    return tag_name


def get_current_tag(user_id):
    session = create_session()
    tag = session.query(Users.current_tag).filter(Users.id == user_id).first()[0]
    session.close()
    return tag


def new_tag(user_id, tag_name):
    session = create_session()
    u_id = get_db_user_id(user_id=user_id)
    tag = Tags(user_id=u_id, tag_name=tag_name)
    if (tag.user_id, tag.tag_name) in session.query(Tags.user_id, Tags.tag_name).all():
        res = session.query(Tags).filter(Tags.user_id == tag.user_id,
                                         Tags.tag_name == tag.tag_name).first()
        session.close()
        return res
    else:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        session.close()
        return tag


def new_file(user_id, tag_name, file_id, f_type, file_name):
    session = create_session()
    tag = new_tag(user_id=user_id, tag_name=tag_name)
    file = Files(file_id=file_id, tag_id=tag.id, type=f_type, name=file_name)
    session.add(file)
    session.commit()
    session.close()


def get_db_user_id(user_id):
    session = create_session()
    user_id = session.query(Users).filter(Users.telegram_id == user_id).first().id
    session.close()
    return user_id


def get_files(tag_id):
    session = create_session()
    tag = session.query(Tags).filter(Tags.id == tag_id).first()
    res = [{'id': i.id, 'f_name': i.name} for i in tag.files]
    session.close()
    return res


def get_file_by_id(id):
    session = create_session()
    file_data = session.query(Files).filter(Files.id == id).first()
    session.close()
    return file_data


def get_tags(user_id):
    session = create_session()
    user = session.query(Users).filter(Users.telegram_id == user_id).first()
    res = [{'tag_id': i.id, 'user_id': i.user_id, 'tag_name': i.tag_name} for i in user.tags]
    session.close()
    return res

