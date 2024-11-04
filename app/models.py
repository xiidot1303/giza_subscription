from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import uuid
from asgiref.sync import sync_to_async


class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(null=True)
    description = models.TextField(blank=True, null=True)
    duration_in_months = models.IntegerField(
        default=1)  # Duration of subscription in months

    def __str__(self):
        return self.name


class Payment(models.Model):
    bot_user = models.ForeignKey(
        "bot.Bot_user", null=True, on_delete=models.CASCADE)
    amount = models.BigIntegerField(null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    payed = models.BooleanField(default=False)
    payment_system = models.CharField(null=True, blank=True, max_length=32)


class Subscription(models.Model):
    bot_user = models.ForeignKey(
        "bot.Bot_user", null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, null=True,
                             blank=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    payment = models.ForeignKey(
        Payment, null=True, blank=True, on_delete=models.CASCADE)
    referral = models.OneToOneField(
        'bot.Referral', null=True, blank=True, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

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


class TelegramChannelAccess(models.Model):
    bot_user = models.OneToOneField(
        "bot.Bot_user", null=True, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)

    @property
    @sync_to_async
    def get_subscription(self):
        return self.subscription
