from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext

from .state.state import waiting
from handlers.forward_channel import forward_to_channel
from handlers.user_link import handle_user_link
from handlers.auto_posting import auto_link
from handlers.cheker_link_handler import save_link_handle, save_link_answer, action_with_link

def register_handlers(dp: Dispatcher):
    from handlers.handlers import (
        send_welcome, manage_users, delete_user_callback, 
        status_posting, edit_status_module, any_post, start_link_post, status_spam, edit_status_spam, handle_caption_post, caption_text_post, subsupdate_handler, log_file_handler
    )
    from .admin.admin_handlers import request_to_join, handle_admin_response, join_member

    router = Router()
    router.message.register(send_welcome, Command(commands=['start', 'help']))
    router.message.register(subsupdate_handler, Command(commands=['subs']))
    router.message.register(manage_users, Command(commands=['users']))
    router.message.register(log_file_handler, Command(commands=['logs']))
    router.callback_query.register(delete_user_callback, lambda cb: cb.data and cb.data.startswith("delete_user:"))
    router.message.register(request_to_join, Command(commands=['join']))
    router.callback_query.register(handle_admin_response, lambda cb: cb.data.startswith('approve_') or cb.data.startswith('deny_'))
    router.message.register(status_posting, Command(commands=['posting']))
    router.callback_query.register(edit_status_module, lambda c: c.data and c.data.startswith('edit_status_'))

    router.message.register(save_link_handle, Command(commands=['saver']))
    router.message.register(save_link_answer, waiting.save_link)
    router.callback_query.register(action_with_link, lambda c: c.data in  ['remove_link', 'save_link', 'back_from_saver'])
    
    # router.callback_query.register(manual_post, lambda c: c.data == 'manual_post')
    router.callback_query.register(start_link_post, lambda c: c.data == 'link_post')
    router.callback_query.register(handle_caption_post, lambda c: c.data == 'caption_post')
    router.callback_query.register(any_post, lambda c: c.data == 'any_post')
    router.callback_query.register(auto_link, lambda c: c.data == 'auto_posting')
    
    router.message.register(handle_user_link, waiting.waiting_video_link)
    router.message.register(caption_text_post, waiting.any_post)

    router.message.register(status_spam, Command(commands=['spam']))
    router.callback_query.register(edit_status_spam, lambda c: c.data and c.data.startswith('spam_status_'))


    router.chat_join_request.register(join_member)
    
    router.message.register(
        forward_to_channel,
        lambda message: message.content_type in [
            types.ContentType.TEXT, 
            types.ContentType.PHOTO, 
            types.ContentType.VIDEO, 
            types.ContentType.ANIMATION, 
            types.ContentType.DOCUMENT
        ]
    )

    dp.include_router(router)
