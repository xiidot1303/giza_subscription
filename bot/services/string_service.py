from bot.services.language_service import *
from app.services.plan_service import *


async def plans_list_string():
    text = ""
    async for plan in SubscriptionPlan.objects.filter(**subscription_plans_filter_dict):
        text += f"▪️ {plan.name} {plan.price} so'm\n"
    return text


async def your_subscription_changed_string(old, new, exp_date):
    text = f"<i>{old}</i> tarifi bo'yicha obunangiz bekor qilindi.\n\n" \
        f"Sizning navbatdagi <i>{new}</i> tarifi bo'yicha obunangiz faollashtirildi va {exp_date} gacha amal qiladi."
    return text
