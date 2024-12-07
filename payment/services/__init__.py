from app.services.payment_service import (
    get_payment_by_id as get_account_by_id,
    payment_pay as account_pay
)
from bot.services import notification_service as notify
from app.services.channel_access_service import successfully_payment_and_create_subscription
from app.models import Payment as Account
from payment.services.payme.subscribe_api import receipts_create_api as get_payme_invoice_id


async def get_invoice_url(payment_id, amount, payment_system):
    if payment_system == 'Payme':
        # create receipt
        invoice_id = await get_payme_invoice_id(payment_id, amount)
        url = f'https://payme.uz/checkout/{invoice_id}'
    # if payment_system == 'Click':
    #     url = get_click_invoice_url(payment_id, amount)
    # if payment_system == 'Uzum':
    #     url = get_uzum_invoice_url(payment_id, amount)
    return url