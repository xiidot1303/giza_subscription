from app.services import *
from app.models import (
    Subscription,
    SubscriptionPlan,
    Payment
)
from bot.models import Referral


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
