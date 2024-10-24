from django.db import models

class Payme_transaction(models.Model):
    payme_trans_id = models.CharField(null=True, blank=False, max_length=64)
    order_id = models.CharField(null=True, blank=False, max_length=128)
    amount = models.BigIntegerField(null=True, blank=True)
    time = models.BigIntegerField(null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)
    perform_time = models.BigIntegerField(null=True, default=0)
    cancel_time = models.BigIntegerField(null=True, default=0)
    STATE_CHOICES = [
        (1, "Транзакция успешно создана, ожидание подтверждения"),
        (2, "Транзакция успешно завершена"),
        (-1, "Транзакция отменена"),
        (-2, "Транзакция отменена после завершения"),
    ]
    state = models.IntegerField(null=True, blank=True, choices=STATE_CHOICES)
    REASON_CHOICES = [
        (1, "Один или несколько получателей не найдены или неактивны в Payme Business."),
        (2, "Ошибка при выполнении дебетовой операции в процессинговом центре."),
        (3, "Ошибка выполнения транзакции."),
        (4, "Транзакция отменена по таймауту."),
        (5, "Возврат денег."),
        (10, "Неизвестная ошибка."),
    ]
    reason = models.IntegerField(null=True, blank=True, choices=REASON_CHOICES)
    test = models.BooleanField(null=True, default=False)

class Card(models.Model):
    bot_user = models.ForeignKey("bot.Bot_user", null=True, on_delete=models.CASCADE)
    number = models.CharField(null=True, max_length=32)
    expire = models.CharField(null=True, max_length=8)
    token = models.CharField(null=True, max_length=1024)
    