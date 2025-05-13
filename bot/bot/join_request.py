from bot.bot import *
from app.services.plan_service import *
from config import WEBAPP_URL
from payment.resources import payment_systems
from payment.services import get_invoice_url
from app.services.payment_service import *


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
    text = await plans_list_string()
    markup = await tariffs_list_keyboard()
    await bot_edit_message_text(update, context, text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)


async def select_plan(update: Update, context: CustomContext):
    data = update.callback_query.data
    _, plan_id = data.split('--')
    # set plan id in user data
    context.user_data["plan_id"] = plan_id

    # get plan
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)
    callbacks = [
        # ('binding card', 'binding_card'),
        ('payment via link', 'payment_via_link'),
        ('change tariff', 'plans_list'),
    ]


    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=await get_word(text, update),
            callback_data=callback
        )]
        for text, callback in callbacks
    ])
    subscriptions_types_text = await get_word('subscription types description', update)
    tariff_text = f"{subscriptions_types_text}\n\n\n<b>✅ {plan.name} {plan.price} so'm</b>"
    await bot_edit_message_text(update, context, tariff_text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)

    return


async def bind_card(update: Update, context: CustomContext):
    await bot_edit_message_reply_markup(update, context)
    text = await get_word("purchase tariff using bind card", update)
    # create buttons for web app
    button = KeyboardButton(
        text=await get_word("bind card", update),
        web_app=WebAppInfo(url=f"{WEBAPP_URL}/subscribe/set-card"),
    )
    markup = ReplyKeyboardMarkup(
        [[button]], resize_keyboard=True, one_time_keyboard=True)
    # await bot_edit_message_reply_markup(update, context, reply_markup=None)
    message: BotMessage = await context.bot.send_message(
        context._user_id, text, reply_markup=markup, parse_mode=ParseMode.HTML)


async def payment_via_link(update: Update, context: CustomContext):
    await bot_edit_message_reply_markup(update, context)
    text = await get_word('select payment service', update)
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=payment_system,
            callback_data=f"select_payment_system--{payment_system}"
        )]
        for payment_system in payment_systems
    ])
    await update_message_reply_text(update, text, reply_markup=markup)


async def select_payment_system(update: Update, context: CustomContext):
    bot_user: Bot_user = await get_object_by_update(update)
    _, payment_system = update.callback_query.data.split('--')
    plan_id = context.user_data["plan_id"]
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)

    # create payment
    payment: Payment = await create_payment(bot_user, plan.price, plan)

    invoice_url = await get_invoice_url(payment.id, payment.amount, payment_system)
    text = "To'lovni amalga oshirish uchun quyidagi havola ustiga bosing 👇"
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="💳 To'lash",
            url=invoice_url
        )
    ]])
    await bot_edit_message_text(update, context, text)
    await bot_edit_message_reply_markup(update, context, reply_markup=markup)
