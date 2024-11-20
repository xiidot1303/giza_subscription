from bot.bot import *
import json
from app.services.payment_service import *
from app.services.plan_service import *
from app.services.subscription_service import *
from app.services.channel_access_service import *
from payment.services.atmos.transaction_api import *
from payment.services.card_service import *
from config import DEBUG


async def web_app_data(update: Update, context: CustomContext) -> None:
    # get data from web app data
    data = json.loads(update.effective_message.web_app_data.data)
    card_data: CardData = DictToClass(data["card_data"])
    plan_id = context.user_data["plan_id"]
    channel_id = context.user_data["channel_id"]
    # get subscription plan object
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)
    # get bot user by update
    bot_user: Bot_user = await get_user_by_update(update)

    # create payment
    payment: Payment = await create_payment(bot_user, plan.price)
    try:
        # create transaction
        transaction_id = await create_transaction_api(payment.id, payment.amount)
        print(card_data, transaction_id)
        pre_apply = await pre_apply_transaction_api(transaction_id, card_data.card_token)
        print(pre_apply)
        assert pre_apply["result"]["code"] == "OK"
        # pay transacrion
        transaction_data = await apply_transaction_api(transaction_id)
        print(transaction_data)
        assert transaction_data["result"]["code"] == "OK"
    
        error = None
    except Exception as ex:
        error = ex

    # update payment object because it changed by merchant api
    await payment.arefresh_from_db()

    if DEBUG:
        payment.payed = True
        await payment.asave()

    if not error and payment.payed:
        # successfullt payment, approve channel join request

        # create or update card of the user
        await update_card_of_bot_user(bot_user, card_data)

        # create subscription
        subscription: Subscription = await create_subscription(
            bot_user, plan, payment
        )

        # approve channel join request
        await context.bot.approveChatJoinRequest(
            chat_id=channel_id,
            user_id=bot_user.user_id
        )

        # create telegram channel access
        await give_channel_access(bot_user, subscription)

        # check referral available of this user
        if referral := await bot_user.get_referral:
            # check for this referral did not give bonus subscription
            if await Subscription.objects.filter(referral__id=referral.id).aexists():
                # dont give bonus
                pass
            else:
                # give bonus to referrer
                referrer: Bot_user = await referral.get_referrer
                # create subscription
                subscription: Subscription = await create_subscription(
                    bot_user=referrer,
                    referral=referral
                )
                # send notification about that bonus given
                given_bonus = await GetText.on(Text.given_bonus)
                await send_newsletter(bot, referrer.user_id, given_bonus)

                # give telegram channel access to referrer, if doesn't exist
                channel_access, created = await give_channel_access(referrer, subscription)
                if created:
                    joined_to_channel_text = await GetText.on(Text.joined_to_channel)
                    markup = await build_keyboard(update, [], 1, back_button=False)
                    try:
                        await context.bot.send_message(referrer.user_id, joined_to_channel_text, reply_markup=markup)
                    except:
                        None

        text = await GetText.on(Text.joined_to_channel)
        markup = await build_keyboard(update, [], 1, back_button=False)
        await update_message_reply_text(update, text, reply_markup=markup)

    elif error:
        # error in payment
        text = await GetText.on(Text.error_in_payment)
        await update_message_reply_text(update, text)
