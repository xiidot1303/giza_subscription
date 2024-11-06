from app.services.channel_access_service import *
from app.services.subscription_service import *
from app.services.payment_service import *
from payment.services.payme.subscribe_api import *
from payment.services.card_service import *
from bot.utils.bot_functions import send_newsletter, bot
from config import DEBUG
from bot.services.text_service import *
from bot.utils.keyboards import change_card_keyboard

async def check_subscription():
    async for subscription in Subscription.objects.filter(
            **filter_active_ended_subscriptions_dict):
        # ready some variables
        plan: SubscriptionPlan = await subscription.get_plan
        bot_user: Bot_user = await subscription.get_bot_user
        card: Card = await get_card_of_bot_user(bot_user)
        # create payment
        payment: Payment = await create_payment(bot_user, plan.price)
        # create receipt
        receipt_id = await receipts_create_api(payment.id, payment.amount)
        # pay receipt
        receipt_pay_data = await receipts_pay_api(receipt_id, card.token)

        # update payment object because it changed by merchant api
        await payment.arefresh_from_db()

        if DEBUG:
            payment.payed = True
            await payment.asave()

        markup = None
        if "result" in receipt_pay_data and payment.payed:
            # successfully payment

            # create new subscription
            new_subscription = await create_subscription(bot_user, plan, payment)
            # update telegram channel access
            await update_channel_access(subscription, new_subscription)


            # send notification about successfully added new subscription
            text = await GetText.on(Text.subscription_renewed)

        else:  # can not charge monthly amount
            # check subscription end date is past more than 3 days
            days_passed = (timezone.now() - subscription.end_date).days
            if days_passed >= 3:
                # remove user from telegram channel
                await remove_user_from_channel(subscription)
                text = await GetText.on(Text.banned)

            else:
                # send alert to user about can not charge amount
                text = await GetText.on(Text.cannot_charge)
                markup = await change_card_keyboard(bot_user)

        await send_newsletter(bot, bot_user.user_id, text, reply_markup=markup)