from sqlalchemy.orm import sessionmaker
from db.model import *


def log_subscriber(user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id):
    engine = create_engine('sqlite:///users.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    exists = session.query(ChannelJoinRequest).filter_by(user_id=user_id).first()
    if exists:
        session.close()
        return

    new_user = ChannelJoinRequest(
        user_id=user_id,
        username=username,
        full_name=full_name,
        first_name=first_name,
        last_name=last_name,
        is_bot=is_bot,
        phone_number=phone_number,
        bio=bio,
        chat_id=chat_id
    )
    session.add(new_user)
    session.commit()
    session.close()
