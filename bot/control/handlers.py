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
    main, join_request, web_app, subscription, login, survey
)

exceptions_for_filter_text = (~filters.COMMAND) & (
    ~filters.Text(lang_dict['main menu']))

main_menu = MessageHandler(filters.Text(lang_dict['main menu']), main.start)

login_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text(lang_dict['registration']), login._to_the_getting_name)
    ],
    states={
        GET_NAME: [
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.Text(lang_dict['back']), login._to_the_getting_name),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_contact)
        ]
    },
    fallbacks=[
        CommandHandler("start", login.start)
    ],
    name="login",
    # persistent=True
)

channel_join_request_handler = ChatJoinRequestHandler(
    join_request.channel_join_request)

web_app_data_handler = MessageHandler(
    filters.StatusUpdate.WEB_APP_DATA, web_app.web_app_data)

handlers = [
    CommandHandler("start", main.start),
    login_handler,
    main_menu,
    channel_join_request_handler,
    web_app_data_handler,
    MessageHandler(filters.VIDEO_NOTE, main.get_video_note_id),
    MessageHandler(filters.VIDEO, main.get_video_id),
    # Callback query handlers
    CallbackQueryHandler(join_request.plans_list, pattern=".*plans_list.*"),
    CallbackQueryHandler(join_request.select_plan,
                         pattern=".*subscription_plan.*"),
    CallbackQueryHandler(subscription.cancel_subscription, pattern=".*cancel_subscription.*"),
    CallbackQueryHandler(main.bot_delete_message, pattern="delete_current_message"),
    CallbackQueryHandler(main.start_instruction, pattern="start_instruction"),
    CallbackQueryHandler(survey.get_survey_result, pattern=".*survey.*")
]
