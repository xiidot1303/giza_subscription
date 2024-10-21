from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField(blank=True, null=True)
    duration_in_months = models.IntegerField(default=1)  # Duration of subscription in months

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    successful = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_date}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months = self.plan.duration_in_months)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.active}"

class TelegramChannelAccess(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Invoice for {self.user.username} on {self.invoice_date}"
