from bot.bot import *
from app.services.plan_service import *
from config import WEBAPP_URL
from telegram import User

async def channel_join_request(update: Update, context: CustomContext):
    # create bot user if doesnt exist 
    user: User = update.effective_user
    await Bot_user.objects.aget_or_create(
        user_id = user.id,
        defaults={
            "name": user.first_name,
            "firstname": user.first_name,
            "lang": "uz",
        }
    )


    text = "start text"
    i_button = InlineKeyboardButton(
        text=await get_word('tariffs', update),
        callback_data="plans_list"
    )
    # set channel id to user data
    context.user_data["channel_id"] = update.effective_chat.id
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
    # set plan id in user data
    context.user_data["plan_id"] = plan_id
    # create buttons for web app
    button = KeyboardButton(
        text=await get_word("Pay for plan", update),
        web_app=WebAppInfo(url=f"{WEBAPP_URL}/subscribe/set-card"),
    )
    text = "purchase"
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await bot_edit_message_reply_markup(update, context, reply_markup=None)
    await bot_send_message(update, context, text, reply_markup=markup)
