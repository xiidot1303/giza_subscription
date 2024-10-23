from bot.bot import *
from app.services.plan_service import *
from config import WEBAPP_URL


async def channel_join_request(update: Update, context: CustomContext):
    text = "start text"
    i_button = InlineKeyboardButton(
        text=await get_word('tariffs', update),
        callback_data="plans_list"
    )
    markup = InlineKeyboardMarkup([[i_button]])
    await bot_send_message(update, context, text, reply_markup=markup)


async def plans_list(update: Update, context: CustomContext):
    text = await plans_list_string()

    i_buttons = [
        [
            InlineKeyboardButton(
                text=plan.name,
                callback_data=f"subscription_plan--{plan.id}"
            )
        ]
        async for plan in SubscriptionPlan.objects.filter(**subscription_plans_filter_dict)
    ]
    markup = InlineKeyboardMarkup(i_buttons)
    await bot_edit_message_text(update, context, text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)


async def select_plan(update: Update, context: CustomContext):
    data = update.callback_query.data
    _, plan_id = data.split('--')
    i_button = InlineKeyboardButton(
        text=await get_word("Pay for plan", update),
        web_app=WebAppInfo(url=f"{WEBAPP_URL}?subscription_plan_id={plan_id}")
    )
    text = "purchase"
    markup = InlineKeyboardMarkup([[i_button]])
    await bot_edit_message_text(update, context, text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)
