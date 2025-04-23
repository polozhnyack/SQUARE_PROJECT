from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ChannelJoinRequest(Base):
    __tablename__ = 'channel_join_requests'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_bot = Column(Boolean)
    phone_number = Column(String)
    bio = Column(String)
    chat_id = Column(Integer)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)