from aiogram.fsm.state import StatesGroup, State


class waiting(StatesGroup):
    waiting_video_link = State()
    caption_text_post = State()
    any_post = State()
    save_link = State()
    action_link = State()