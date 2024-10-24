class Errors:
    ORDER_NOT_FOUND = {
        "code": -31050,
        "message": {
            "ru": "ID не найден",
            "uz": "ID ro'yhatda yo'q",
            "en": "ID not found",
        }
    }

    INCORRECT_AMOUNT = {
        "code": -31001,
        "message": {
            "ru": "Неверная сумма.",
            "uz": "Noto'gri summa.",
            "en": "Incorrect amount."
        }
    }

    TRANSACTION_NOT_FOUND = {
        "code": -31003,
        "message": {
            "ru": "Транзакция не найдена.",
            "uz": "Транзакция не найдена.",
            "en": "Транзакция не найдена."
        }
    }

    CANNOT_PERFORM_OPERATION = {
        "code": -31008,
        "message": {
            "ru": "Невозможно выполнить данную операцию.",
            "uz": "Невозможно выполнить данную операцию.",
            "en": "Невозможно выполнить данную операцию."
        }
    }

    CANNOT_CANCEL_TRANSACTION = {
        "code": -31007,
        "message": {
            "ru": "Заказ выполнен. Невозможно отменить транзакцию.",
            "uz": "Заказ выполнен. Невозможно отменить транзакцию.",
            "en": "Заказ выполнен. Невозможно отменить транзакцию.",
        }
    }

    INCORRECT_TIME = {
        "code": -31060,
        "message": {
            "ru": "incorrect time",
            "uz": "incorrect time",
            "en": "incorrect time",
        }
    }

    NOT_ENOUGH_PRIVILEGES = {
        "code": -32504,
        "message": {
            "ru": "Недостаточно привилегий для выполнения метода.",
            "uz": "Недостаточно привилегий для выполнения метода.",
            "en": "Недостаточно привилегий для выполнения метода.",
        }
    }

    REQUEST_IS_NOT_POST = {
        "code": -32300,
        "message": {
            "ru": "Request method is not POST.",
            "uz": "Request method is not POST.",
            "en": "Request method is not POST.",
        }
    }

class Results:
    def CHECKPERFORM_TRANSACTION(name, phone):
        r = {
            "allow": True,
            "additional": {
                "name": name,
                "phone": phone
            }
        }
        return r
    
    def CREATE_TRANSACTION(create_time, transaction, state):
        r = {
            "create_time" : create_time,
            "transaction" : transaction,
            "state" : state
        }
        return r
    
    def PERFORM_TRANSACTION(transaction, perform_time, state):
        r = {
            "transaction" : transaction,
            "perform_time" : perform_time,
            "state" : state
        }
        return r
    
    def CANCEL_TRANSACTION(transaction, cancel_time, state):
        r = {
            "transaction" : transaction,
            "cancel_time" : cancel_time,
            "state" : state
        }
        return r
    
    def CHECK_TRANSACTION(create_time, perform_time, cancel_time, transaction, state, reason):
        r = {
            "create_time" : create_time,
            "perform_time" : perform_time,
            "cancel_time" : cancel_time,
            "transaction" : transaction,
            "state" : state,
            "reason" : reason
        }
        return r
    
    def GET_STATEMENT(transactions):
        r = {
            "transactions" : [
                {
                    "id" : t.payme_trans_id,
                    "time" : t.time,
                    "amount" : t.amount,
                    "account" : {
                        "callsign" : t.driver.callsign
                    },
                    "create_time" : t.create_time,
                    "perform_time" : t.perform_time,
                    "cancel_time" : t.cancel_time,
                    "transaction" : str(t.id),
                    "state" : t.state,
                    "reason" : t.reason,
                    # "receivers" : [
                        # {
                        #     "id" : "5305e3bab097f420a62ced0b",
                        #     "amount" : 200000
                        # },
                    # ]
                }
                for t in transactions
            ]
        }
        return r