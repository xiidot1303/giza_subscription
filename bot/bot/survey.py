from bot.bot import *
from app.services.survey_service import create_survey


async def get_survey_result(update: Update, context: CustomContext):
    data = update.callback_query.data
    _, answer = data.split('--')
    bot_user: Bot_user = await get_object_by_update(update)
    # create survey object
    await create_survey(bot_user, answer)
    
    await bot_answer_callback_query(update, context, "✅ Qabul qilindi!", show_alert=False)
    await bot_edit_message_reply_markup(update, context)
