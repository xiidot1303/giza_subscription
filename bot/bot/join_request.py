from bot.bot import *
from app.services.plan_service import *
from config import WEBAPP_URL


async def channel_join_request(update: Update, context: CustomContext):
    # check user already has access to channel
    if await has_channel_access(update.effective_user.id):
        await update.chat_join_request.approve()
        return

    text = await GetText.on(Text.after_join_request)
    i_button = InlineKeyboardButton(
        text=await get_word('tariffs', update),
        callback_data="plans_list"
    )
    # set channel id to user data
    context.user_data["channel_id"] = update.effective_chat.id
    markup = InlineKeyboardMarkup([[i_button]])
    await bot_send_message(update, context, text, reply_markup=markup)


async def plans_list(update: Update, context: CustomContext):
    if "--" in update.callback_query.data:
        _, message_id = update.callback_query.data.split('--')
        # delete message which bottom of the current message
        await context.bot.delete_message(context._user_id, message_id)
        
    text = await plans_list_string()

    i_buttons = [
        [
            InlineKeyboardButton(
                text=plan.name,
                callback_data=f"subscription_plan--{plan.id}"
            )
        ]
        async for plan in SubscriptionPlan.objects.filter(
            **subscription_plans_filter_dict).order_by("duration_in_months")
    ]
    markup = InlineKeyboardMarkup(i_buttons)
    await bot_edit_message_text(update, context, text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)


async def select_plan(update: Update, context: CustomContext):
    data = update.callback_query.data
    _, plan_id = data.split('--')
    # set plan id in user data
    context.user_data["plan_id"] = plan_id
    # get plan
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)
    # create buttons for web app
    button = KeyboardButton(
        text=await get_word("Pay for plan", update),
        web_app=WebAppInfo(url=f"{WEBAPP_URL}/subscribe/set-card"),
    )
    tariff_text = f"✅ {plan.name} {plan.price} so'm"
    text = await get_word("purchase tariff", update)
    markup = ReplyKeyboardMarkup(
        [[button]], resize_keyboard=True, one_time_keyboard=True)
    # await bot_edit_message_reply_markup(update, context, reply_markup=None)
    await bot_edit_message_text(update, context, tariff_text)
    message: BotMessage = await bot_send_message(update, context, text, reply_markup=markup)

    i_button = InlineKeyboardButton(
        text=await get_word('change tariff', update),
        callback_data=f"plans_list--{message.message_id}"
    )
    markup = InlineKeyboardMarkup([[i_button]])

    await bot_edit_message_reply_markup(update, context, reply_markup=markup)