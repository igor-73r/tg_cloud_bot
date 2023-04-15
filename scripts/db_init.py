from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

Base = declarative_base()

engine = create_engine("sqlite:///cloud.db")

session = Session(bind=engine)


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
    tag_name = Column(String(50), nullable=False)
    files = relationship('Files')

    def __repr__(self):
        return f"TagData(id={self.id}, user_id={self.user_id}, tag={self.tag_name})"



class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    type = Column(String(20), nullable=False)



Base.metadata.create_all(engine)