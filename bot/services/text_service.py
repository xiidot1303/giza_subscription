from bot.models import Text
import json


class GetText:
    file_path = "bot/resources/text.json"
    data = {}

    @classmethod
    async def update_data(cls):
        cls.data = await cls._load_json(cls)

    async def _load_json(cls):
        """
        Private method to load JSON data from the file.
        """
        try:
            with open(cls.file_path, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print(f"Error: File {cls.file_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: File {cls.file_path} is not valid JSON.")
            return {}

    @classmethod
    async def on(cls, model_field):
        if not cls.data:
            cls.data = await cls._load_json(cls)
        attribute_name = model_field.field.name
        """
        Public method to get the value of a specified attribute.
        """
        text = cls.data.get(attribute_name, attribute_name)
        return text if text else attribute_name
