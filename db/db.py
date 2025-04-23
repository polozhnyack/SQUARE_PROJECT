from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import setup_logger

logger = setup_logger()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)


class Database:
    def __init__(self, db_path='sqlite:///users.db'):
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, user_id, first_name, last_name):
        session = self.Session()
        try:
            # Проверяем, есть ли уже такой пользователь
            existing_user = session.query(User).filter_by(user_id=user_id).first()
            if existing_user:
                logger.info(f"Пользователь с ID {user_id} уже существует.")
                return

            user = User(user_id=user_id, first_name=first_name, last_name=last_name)
            session.add(user)
            session.commit()
            logger.info(f"Пользователь {first_name} добавлен в базу данных.")
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при добавлении пользователя: {e}")
        finally:
            session.close()


    def remove_user(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).filter_by(user_id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при удалении пользователя: {e}")
        finally:
            session.close()

    def get_user(self, user_id):
        session = self.Session()
        try:
            return session.query(User).filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(f"Ошибка при получении пользователя: {e}")
            return None
        finally:
            session.close()

    def get_all_users(self):
        session = self.Session()
        try:
            return session.query(User).all()
        except Exception as e:
            logger.error(f"Ошибка при получении всех пользователей: {e}")
            return []
        finally:
            session.close()
