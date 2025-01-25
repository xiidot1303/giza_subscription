from app.services.channel_access_service import *
from app.services.subscription_service import *
from app.services.payment_service import *
from payment.services.atmos.transaction_api import *
from payment.services.card_service import *
from bot.utils.bot_functions import send_newsletter
from bot.control.updater import application
from config import DEBUG
from bot.services.text_service import *
from bot.utils.keyboards import change_card_keyboard


async def check_subscription():
    async for subscription in Subscription.objects.filter(
            **filter_active_ended_subscriptions_dict):
        # ready some variables
        plan: SubscriptionPlan = await subscription.get_plan
        bot_user: Bot_user = await subscription.get_bot_user
        markup = None 
        if plan:
            # check subscription end date is past more than 3 days
            days_passed = (timezone.now() - subscription.end_date).days
            if days_passed >= 3:
                # remove user from telegram channel
                await remove_user_from_channel(subscription, application.bot)
                text = await GetText.on(Text.banned)
            else:
                # check card is available of user
                card: Card = await get_card_of_bot_user(bot_user)
                if card.token:
                    # charge via card
                    markup = await extend_or_cancel_subscription_keyboard(subscription.id)
                    text = await extend_subscription_string(plan)
                else:
                    # charge via invoice
                    pass


        else:  # the subscription is bonus
            if next_subscription := await get_next_active_subscription(subscription):
                await update_channel_access(subscription, next_subscription)
                text = await GetText.on(Text.subscription_renewed)
            else:
                await remove_user_from_channel(subscription, application.bot)
                text = await GetText.on(Text.banned)

        await send_newsletter(application.bot, bot_user.user_id, text, reply_markup=markup)
