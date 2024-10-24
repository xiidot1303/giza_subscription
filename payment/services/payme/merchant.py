# from app.services.order_service import *
from payment.resources.payme_responses import Errors, Results
from payment.utils import time_ts
from payment.services.payme.transaction import *

def get_order_by_id(): return 0

def CheckPerformTransaction(amount, order_id):
    if order:=get_order_by_id(order_id):
        if trans_obj:=get_active_transaction_by_order_id(order_id):
            return None, Errors.ORDER_NOT_FOUND
        if int(amount) / 100 != int(order['total']):
            return None, Errors.INCORRECT_AMOUNT
        name = order['username']
        return Results.CHECKPERFORM_TRANSACTION(name, order['phone_number']), None
    else:
        return None, Errors.ORDER_NOT_FOUND
    
def CreateTransaction(id, time, amount, order_id, test):
    if order:=get_order_by_id(order_id):
        if time_ts() - time >= 43200000:
            return {}, Errors.CANNOT_PERFORM_OPERATION
        if trans_obj:=get_active_transaction_by_order_id(order_id):
            if trans_obj.payme_trans_id != id:
                return None, Errors.ORDER_NOT_FOUND
        if int(amount) / 100 != int(order['total']):
            return None, Errors.INCORRECT_AMOUNT
        trans_obj = get_or_create_transaction(id, order,amount/100, time_ts(), time, test)
        create_time = trans_obj.create_time
        trans_id = str(trans_obj.id)
        state = trans_obj.state
        return Results.CREATE_TRANSACTION(create_time, trans_id, state), None
    else:
        return None, Errors.ORDER_NOT_FOUND

def PerformTransaction(id):
    if trans_obj:=get_transaction_by_payme_trans_id(id):
        # check transactio  status
        if trans_obj.state == 1:
            # check time out
            if time_ts() - trans_obj.create_time >= 43200000:
                cancel_transaction(trans_obj, -1, 4)
                return {}, Errors.CANNOT_PERFORM_OPERATION
            # send transaction to yandex api
            if not trans_obj.test:
                try:
                    # change order status in js
                    success = payme_accept_order(trans_obj.order_id)['success']
                    assert success == 1
                except:
                    cancel_transaction(trans_obj, -1, 10)
                    return None, Errors.CANNOT_PERFORM_OPERATION
            # end transaction
            perform_transaction(trans_obj)
        else:
            if trans_obj.state != 2:
                return None, Errors.CANNOT_PERFORM_OPERATION

        # success return
        trans_id = str(trans_obj.id)
        perform_time = trans_obj.perform_time
        state = trans_obj.state
        return Results.PERFORM_TRANSACTION(trans_id, perform_time, state), None
    else:
        return None, Errors.TRANSACTION_NOT_FOUND

def CancelTransaction(id, reason):
    if trans_obj:=get_transaction_by_payme_trans_id(id):
        if trans_obj.state == 1:
            cancel_transaction(trans_obj, -1, reason)
        elif trans_obj.state == 2:
            cancel_transaction(trans_obj, -2, reason)
            # return None, Errors.CANNOT_CANCEL_TRANSACTION
        # success return
        trans_id = str(trans_obj.id)
        cancel_time = trans_obj.cancel_time
        state = trans_obj.state
        return Results.CANCEL_TRANSACTION(trans_id, cancel_time, state), None
    else:
        return None, Errors.TRANSACTION_NOT_FOUND
    
def CheckTransaction(id):
    if trans_obj:=get_transaction_by_payme_trans_id(id):
        result = Results.CHECK_TRANSACTION(
            trans_obj.create_time, trans_obj.perform_time,
            trans_obj.cancel_time, str(trans_obj.id),
            trans_obj.state, trans_obj.reason
        )
        return result, None
    else:
        return None, Errors.TRANSACTION_NOT_FOUND
    
def GetStatement(from_, to):
    transactions = filter_transactions_by_createtime_period(from_, to)
    return Results.GET_STATEMENT(transactions), None