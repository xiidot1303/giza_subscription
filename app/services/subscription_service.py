from app.services import *
from app.models import (
    Subscription,
    SubscriptionPlan,
    Payment
)
from bot.models import Referral


async def get_subscription_by_id(id):
    obj = await Subscription.objects.filter(id=id).afirst()
    return obj


async def create_subscription(
    bot_user: Bot_user,
    plan: SubscriptionPlan = None,
    payment: Payment = None,
    referral: Referral = None
) -> Subscription:
    obj = await Subscription.objects.acreate(
        bot_user=bot_user, plan=plan,
        payment=payment, referral=referral
    )
    return obj

filter_active_ended_subscriptions_dict = {
    "end_date__lte": timezone.now(),
    "active": True
}


async def get_last_bonus_subscription(bot_user: Bot_user):
    obj = await Subscription.objects.filter(
        bot_user=bot_user, active=True).exclude(
            referral=None).order_by('end_date').alast()
    return obj


async def get_next_active_subscription(current_subscription: Subscription):
    bot_user: Bot_user = await current_subscription.get_bot_user
    obj = await Subscription.objects.filter(
        bot_user=bot_user, active=True).exclude(
            id=current_subscription.id).order_by('start_date').afirst()
    return obj
