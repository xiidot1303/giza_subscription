from app.models import Setting


async def get_settings():
    return await Setting.objects.aget()


async def get_offer_url():
    if setting := await Setting.objects.filter().afirst():
        return setting.offer.url
    else:
        return ""


async def get_support_url():
    if setting := await Setting.objects.filter().afirst():
        return setting.support
    else:
        return ""
