from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import uuid

class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(null=True)
    description = models.TextField(blank=True, null=True)
    duration_in_months = models.IntegerField(default=1)  # Duration of subscription in months

    def __str__(self):
        return self.name

class Payment(models.Model):
    bot_user = models.ForeignKey("bot.Bot_user", null=True, on_delete=models.CASCADE)
    amount = models.BigIntegerField(null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    payed = models.BooleanField(default=False)



class Subscription(models.Model):
    bot_user = models.ForeignKey("bot.Bot_user", null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    payment = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months = self.plan.duration_in_months)
        super().save(*args, **kwargs)


class TelegramChannelAccess(models.Model):
    bot_user = models.OneToOneField("bot.Bot_user", null=True, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)