from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler,
    ChatJoinRequestHandler
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *

from bot.bot import (
    main, join_request
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

start = CommandHandler('start', main.start)

channel_join_request_handler = ChatJoinRequestHandler(join_request.channel_join_request)

handlers = [
    start,
    channel_join_request_handler,
    
    # Callback query handlers
    CallbackQueryHandler(join_request.plans_list, pattern="plans_list"),
    CallbackQueryHandler(join_request.select_plan, pattern=".*subscription_plan.*"),
]