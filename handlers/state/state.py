from aiogram.fsm.state import StatesGroup, State


class waiting(StatesGroup):
    waiting_video_link = State()
    any_post = State()
    save_link = State()
    action_link = State()
    activPosting = State()
    caption_post = State()