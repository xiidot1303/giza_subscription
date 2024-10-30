from django.db.models.signals import post_save
from django.dispatch import receiver
from bot.models import Text
from django.core.serializers.json import DjangoJSONEncoder
from bot.services.text_service import GetText
import json
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Text)
def update_json_file(sender, instance, created, **kwargs):
    # Convert a Django model instance into a dictionary of all field names and values.
    data = {}
    for field in instance._meta.get_fields():
        if hasattr(instance, field.name):  # Check if instance has this field
            data[field.name] = getattr(instance, field.name)  # Get field value

    file_path = "bot/resources/text.json"
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, cls=DjangoJSONEncoder, indent=4)
    
    # update object 
    async_to_sync(GetText.update_data)()