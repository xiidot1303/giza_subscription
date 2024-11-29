from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import uuid
from asgiref.sync import sync_to_async


class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.BigIntegerField(null=True, verbose_name="Цена")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание")
    duration_in_months = models.IntegerField(
        default=1, verbose_name="Длительность (в месяцах)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class Payment(models.Model):
    bot_user = models.ForeignKey(
        "bot.Bot_user", null=True, on_delete=models.CASCADE, verbose_name="Пользователь бота"
    )
    amount = models.BigIntegerField(null=True, verbose_name="Сумма")
    payment_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата платежа")
    payed = models.BooleanField(default=False, verbose_name="Оплачено?")
    payment_system = models.CharField(
        null=True, blank=True, max_length=32, verbose_name="Платежная система"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    bot_user = models.ForeignKey(
        "bot.Bot_user", null=True, on_delete=models.CASCADE, verbose_name="Пользователь бота"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Тарифный план"
    )
    start_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateTimeField(null=True, verbose_name="Дата окончания")
    payment = models.ForeignKey(
        Payment, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Платеж"
    )
    referral = models.OneToOneField(
        'bot.Referral', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Реферал"
    )
    active = models.BooleanField(default=True, verbose_name="Активен?")

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.plan:
                self.end_date = self.start_date + \
                    relativedelta(months=self.plan.duration_in_months)
            elif self.referral:
                # check more active subscriptions is available
                if last_active_subscription := Subscription.objects.filter(
                    active=True).exclude(
                        id=self.id).order_by('end_date').last():
                    self.start_date = last_active_subscription.end_date

                self.end_date = self.start_date + relativedelta(months=1)
        super().save(*args, **kwargs)

    @property
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user

    @property
    @sync_to_async
    def get_plan(self):
        return self.plan

    @property
    @sync_to_async
    def get_plan_name(self):
        return self.plan.name if self.plan else "BONUS"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class TelegramChannelAccess(models.Model):
    bot_user = models.OneToOneField(
        "bot.Bot_user", null=True, on_delete=models.PROTECT, verbose_name="Пользователь бота"
    )
    subscription = models.OneToOneField(
        Subscription, on_delete=models.PROTECT, verbose_name="Подписка"
    )

    @property
    @sync_to_async
    def get_subscription(self):
        return self.subscription

    class Meta:
        verbose_name = "Доступ к каналу"
        verbose_name_plural = "Подписчики канала"


class Setting(models.Model):
    offer = models.FileField(null=True, blank=True, verbose_name="Оферта")
    support = models.CharField(null=True, blank=True, max_length=255, verbose_name="Служба поддержки (Ссылка на аккаунт Telegram)")
    start_video_note_id = models.CharField(null=True, blank=True, max_length=255)
    instruction_video_note_id = models.CharField(null=True, blank=True, max_length=255)
    instruction_of_channel_video_id = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
