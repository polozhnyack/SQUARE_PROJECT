from aiogram.fsm.state import StatesGroup, State


class waiting(StatesGroup):
    waiting_video_link_sosalkino = State()
    caption_text_post = State()
    any_post = State()