import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    connection_string = "sqlite:///cloud.db"
    engine = sa.create_engine(connection_string)
    __factory = orm.sessionmaker(bind=engine)

    from scripts.db_init import Users, Tags, Files

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
