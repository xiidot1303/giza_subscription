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

    def __str__(self):
        return f"{self.bot_user.name} - {self.amount} - {self.payment_date}"

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

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.active}"

class TelegramChannelAccess(models.Model):
    bot_user = models.OneToOneField("bot.Bot_user", null=True, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    has_access = models.BooleanField(default=False)

    def check_access(self):
        """
        Checks if the user should have access to the channel based on their subscription.
        """
        if self.subscription.active and timezone.now() <= self.subscription.end_date:
            self.has_access = True
        else:
            self.has_access = False
        self.save()

    def __str__(self):
        return f"{self.user.username} - {'Access' if self.has_access else 'No Access'}"