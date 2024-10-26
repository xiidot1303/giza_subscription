from app.services import *
from app.models import (
    Subscription,
    SubscriptionPlan,
    Payment
)


async def create_subscription(
    bot_user: Bot_user,
    plan: SubscriptionPlan,
    payment: Payment
) -> Subscription:
    obj = await Subscription.objects.acreate(
        bot_user=bot_user, plan=plan, payment=payment
    )
    return obj
