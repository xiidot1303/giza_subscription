from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from app.models import *
from solo.admin import SingletonModelAdmin

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_in_months')
    search_fields = ('name',)
    list_filter = ('duration_in_months',)
    ordering = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bot_user', 'amount', 'payment_date', 'payed')
    list_filter = ('payed', 'payment_date')
    search_fields = ('bot_user__name',)
    ordering = ('-payment_date',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('bot_user', 'plan', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date', 'end_date', 'plan')
    search_fields = ('bot_user__username', 'plan__name')
    ordering = ('-start_date',)

@admin.register(TelegramChannelAccess)
class TelegramChannelAccessAdmin(admin.ModelAdmin):
    list_display = ('bot_user', 'subscription')

admin.site.register(Setting, SingletonModelAdmin)

# Customizing the Admin Site settings
admin.site.site_header = _("Giza Subscription Management System Admin")
admin.site.site_title = _("Giza Subscription Management Admin")
admin.site.index_title = _("Welcome to the Giza Subscription Management System Admin")
