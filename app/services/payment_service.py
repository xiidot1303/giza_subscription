from app.services import *
from bot.models import Bot_user
from app.models import Payment


async def create_payment(bot_user: Bot_user, amount):
    obj = await Payment.objects.acreate(
        bot_user=bot_user, amount=amount
    )
    return obj


async def get_payment_by_id(id: int | str) -> Payment | None:
    obj = await Payment.objects.filter(id=id).afirst()
    return obj


async def payment_pay(payment: Payment, payment_system):
    payment.payed = True
    payment.payment_system = payment_system
    await payment.asave()


@sync_to_async
def filter_payed_payments_by_bot_user_list(bot_user: Bot_user):
    query_list = list(Payment.objects.filter(
        bot_user__id=bot_user.id, payed=True
        ).values()
    )
    return query_list
