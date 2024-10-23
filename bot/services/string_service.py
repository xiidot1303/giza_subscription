from bot.services.language_service import *
from app.services.plan_service import *

async def plans_list_string():
    text = ""
    async for plan in SubscriptionPlan.objects.filter(**subscription_plans_filter_dict):
        text += f"▪️ {plan.name} {plan.price} so'm\n"
    return text