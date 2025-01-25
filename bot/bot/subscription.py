from bot.bot import *
from app.services.subscription_service import *
from app.services.channel_access_service import *
from app.services.payment_service import *
from payment.services.atmos.transaction_api import *
from payment.services.card_service import *
from bot.services.text_service import *
from bot.utils.keyboards import change_card_keyboard


async def extend_subscription(update: Update, context: CustomContext):
    await bot_edit_message_reply_markup(update, context)

    *args, subscription_id = str(update.callback_query.data).split("--")
    subscription: Subscription = await get_subscription_by_id(subscription_id)
    bot_user: Bot_user = await subscription.get_bot_user
    plan: SubscriptionPlan = await subscription.get_plan

    # create payment
    payment: Payment = await create_payment(bot_user, plan.price)
    try:
        card: Card = await get_card_of_bot_user(bot_user)
        # create receipt
        transaction_id = await create_transaction_api(payment.id, payment.amount)
        # pay receipt
        pre_apply = await pre_apply_transaction_api(transaction_id, card.token)
        assert pre_apply["result"]["code"] == "OK"
        transaction_data = await apply_transaction_api(transaction_id)
        assert transaction_data["result"]["code"] == "OK"
        payment.payed = True
        await payment.asave()
        error = None
    except Exception as ex:
        error = ex
    # update payment object because it changed by merchant api
    await payment.arefresh_from_db()
    markup = None
    if not error and payment.payed:
        # successfully payment
        # create new subscription
        new_subscription = await create_subscription(bot_user, plan, payment)
        # update telegram channel access
        await update_channel_access(subscription, new_subscription)
        # send notification about successfully added new subscription
        text = await GetText.on(Text.subscription_renewed)
    else:  # can not charge monthly amount
        # send alert to user about can not charge amount
        text = await GetText.on(Text.cannot_charge)
        markup = await change_card_keyboard(bot_user)

    await context.bot.send_message(update.effective_user.id, text, reply_markup=markup)


async def cancel_subscription(update: Update, context: CustomContext):
    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context)

    *args, subscription_id = str(update.callback_query.data).split("--")
    subscription: Subscription = await get_subscription_by_id(subscription_id)
    bot_user: Bot_user = await subscription.get_bot_user

    # cancel subscription
    # if active subcriptions available in the next, set subscription or remove user from channel
    if next_subscription := await get_next_active_subscription(subscription):
        await update_channel_access(subscription, next_subscription)
        # send message about subscription changed
        expire_date = next_subscription.end_date.strftime("%d.%m.%Y")
        text = await your_subscription_changed_string(
            await subscription.get_plan_name,
            await next_subscription.get_plan_name,
            expire_date
        )
        await update_message_reply_text(update, text)
    else:
        await remove_user_from_channel(subscription, context.bot)
        # send message about successfully deactivated subscription
        text = await get_word('successfully deactivated subscription', update)
        await update_message_reply_text(update, text)
