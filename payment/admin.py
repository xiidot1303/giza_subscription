from django.contrib import admin
from payment.models import *

class Payme_transactionAdmin(admin.ModelAdmin):
    list_display = ['payme_trans_id', 'amount', 'create_time', 'state', 'test']

class CardAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'token']

admin.site.register(Payme_transaction, Payme_transactionAdmin)
admin.site.register(Card, CardAdmin)