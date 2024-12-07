from bot.bot import *
import json
from app.services.payment_service import *
from app.services.plan_service import *
from app.services.subscription_service import *
from app.services.channel_access_service import *
from payment.services.atmos.transaction_api import *
from payment.services.atmos.card_api import remove_card_api
from payment.services.card_service import *
from bot.services.referral_service import referrals_count_of_bot_user
from config import DEBUG


async def web_app_data(update: Update, context: CustomContext) -> None:
    # get data from web app data
    data = json.loads(update.effective_message.web_app_data.data)
    card_data: CardData = DictToClass(data["card_data"])

    try:
        # get bot user by update
        bot_user: Bot_user = await get_user_by_update(update)
        # create or update card of the user
        await update_card_of_bot_user(bot_user, card_data)

        plan_id = context.user_data["plan_id"]
        channel_id = TG_CHANNEL_ID
        # get subscription plan object
        plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)

        # create payment
        payment: Payment = await create_payment(bot_user, plan.price)
        # create transaction
        transaction_id = await create_transaction_api(payment.id, payment.amount)
        pre_apply = await pre_apply_transaction_api(transaction_id, card_data.card_token)
        assert pre_apply["result"]["code"] == "OK", pre_apply
        # pay transacrion
        transaction_data = await apply_transaction_api(transaction_id)
        assert transaction_data["result"]["code"] == "OK", transaction_data

        # set payment as payed
        payment.payed = True
        await payment.asave()

        error = None
    except Exception as ex:
        error = ex

    # update payment object because it changed by merchant api
    # await payment.arefresh_from_db()

    if not error and payment.payed:
        # successfullt payment, approve channel join request
        await successfully_payment_and_create_subscription(
            payment, context.bot, bot_user, plan)

    elif error:
        # remove card
        await remove_card_api(card_data.card_id, card_data.card_token)
        # error in payment
        text = await GetText.on(Text.error_in_payment)
        await update_message_reply_text(update, text, reply_markup=await reply_keyboard_remove())

        # make error text
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text=update.effective_user.first_name,
                url=f"tg://user?id={context._user_id}"
            )
        ]])
        try:
            await context.bot.send_message(
                chat_id=-4664434651, text=str(error), reply_markup=markup
            )
        except:
            None
