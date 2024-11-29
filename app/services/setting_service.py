from app.models import Setting


async def get_offer_url():
    if setting := await Setting.objects.filter().afirst():
        return setting.offer.url
    else:
        return ""