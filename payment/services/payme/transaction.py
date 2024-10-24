from app.services import *
from payment.models import Payme_transaction as Trans
from payment.utils import time_ts

def get_or_create_transaction(payme_trans_id, order: dict, amount, time, create_time, test) -> Trans:
    obj, created = Trans.objects.get_or_create(payme_trans_id=payme_trans_id)
    if created:
        obj.order_id = order['order_id']
        obj.amount = amount
        obj.time = time
        obj.create_time = create_time
        obj.state = 1
        obj.test = test
        obj.save()
    return obj

def get_transaction_by_payme_trans_id(id):
    try:
        obj = Trans.objects.get(payme_trans_id=id)
        return obj
    except:
        return None

def get_active_transaction_by_order_id(order_id):
    try:
        obj = Trans.objects.get(Q(order_id=order_id) & (Q(state=1) | Q(state=2)))
        return obj
    except:
        return None

def perform_transaction(obj: Trans):
    obj.state = 2
    obj.perform_time = time_ts()
    obj.save()
    return

def cancel_transaction(obj: Trans, state: int, reason: int):
    obj.state = state
    obj.reason = reason
    obj.cancel_time = time_ts()
    obj.save()
    return

def filter_transactions_by_createtime_period(from_, to):
    return Trans.objects.filter(create_time__range = (from_, to), test = False)