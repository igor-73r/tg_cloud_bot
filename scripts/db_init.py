from sqlalchemy import Integer, String, \
    Column, ForeignKey
from sqlalchemy.orm import relationship
from scripts.db_session import SqlAlchemyBase as Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    tags = relationship("Tags")

    def __repr__(self):
        return f"UserData(id={self.id}, tg_id={self.telegram_id}, tags={self.tags})"


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tag_name = Column(String, nullable=False)
    files = relationship('Files')

    def __repr__(self):
        return f"TagData(tag_id={self.id}, user_id={self.user_id}, tag_name={self.tag_name})"



class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    type = Column(String, nullable=False)
    name = Column(String)
