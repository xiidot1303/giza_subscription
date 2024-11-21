from django.core.management.base import BaseCommand
from payment.services.atmos import create_access_token, cache
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Command that delete webhook'

    def handle(self, *args, **options):
        access_token = cache.get("atmos:access_token") or async_to_sync(create_access_token)()
        print(access_token)