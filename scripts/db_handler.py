import sqlalchemy.exc
from scripts.db_init import *
from scripts.db_session import create_session


def new_user(user_id):
    session = create_session()
    user = Users(telegram_id=user_id)
    print(session.query(Users).all())  # TODO DEBUG
    session.add(user)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        print('Уже в базе')  # TODO DEBUG
    session.close()


def new_tag(user_id, tag_name):
    session = create_session()
    u_id = get_db_user_id(user_id=user_id)
    print(u_id)  # TODO DEBUG
    tag = Tags(user_id=u_id, tag_name=tag_name)
    if (tag.user_id, tag.tag_name) in session.query(Tags.user_id, Tags.tag_name).all():
        res = session.query(Tags).filter(Tags.user_id == tag.user_id,
                                         Tags.tag_name == tag.tag_name).first()
        session.close()
        return res
    else:
        print("ЗАШЛИ НЕ ТУДА-------------------")
        session.add(tag)
        session.commit()
        print(session.query(Users).all())  # TODO DEBUG
        session.close()
        return tag


def new_file(user_id, tag_name, file_id, f_type, file_name):
    session = create_session()
    tag = new_tag(user_id=user_id, tag_name=tag_name)
    print(tag)
    file = Files(file_id=file_id, tag_id=tag.id, type=f_type, name=file_name)
    session.add(file)
    session.commit()
    session.close()


def get_db_user_id(user_id):
    session = create_session()
    user_id = session.query(Users).filter(Users.telegram_id == user_id).first().id
    session.close()
    return user_id


def get_files(user_id, tag_name):
    session = create_session()
    tag = session.query(Tags).filter(Tags.user_id == get_db_user_id(user_id=user_id),
                                     Tags.tag_name == tag_name).first()
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
    # res = [i.tag_name for i in user.tags]
    res = [{'tag_id': i.id, 'user_id': i.user_id, 'tag_name': i.tag_name} for i in user.tags]
    print(res)
    session.close()
    return res

