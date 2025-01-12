from bot.services.language_service import *
from app.services.plan_service import *


async def plans_list_string():
    text = "<b>“BIZ BIRGAMIZ🫂” klubi ta’riflar va narxlari!</b>\n\n"
    async for plan in SubscriptionPlan.objects.filter(
            **subscription_plans_filter_dict).order_by("duration_in_months"):
        price = f"{plan.price:,}".replace(",", ".")
        sale_text = plan.sale_text or ""
        text += f"<b>{plan.name} narxi</b> - {price} {sale_text}\n\n"
    return text


async def your_subscription_changed_string(old, new, exp_date):
    text = f"<i>{old}</i> tarifi bo'yicha obunangiz bekor qilindi.\n\n" \
        f"Sizning navbatdagi <i>{new}</i> tarifi bo'yicha obunangiz faollashtirildi va {exp_date} gacha amal qiladi."
    return text


async def extend_subscription_string(plan: SubscriptionPlan):
    text = f"Xurmatli foydalanuvchi, sizning obunangiz yakunlanmoqda. Kanalimizda obunani davom ettirmoqchi bo'lsangiz " \
        f"tarifingiz uchun to'lovni amalga oshiring.\n\nSizning tarifingiz: <b>{plan.name} - {plan.price} so'm</b>\n\n" \
            f"Ushbu summani bizga biriktirgan kartangizdan yechib olinishini tasdiqlaysizmi?"
    return text