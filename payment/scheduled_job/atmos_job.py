from payment.services.atmos import *
from django.core.cache import cache

async def update_access_token():
    # pass if access token is available
    if not await cache.aget("atmos:access_token"):
        if refresh_token := await cache.aget("atmos:access_token:copy"):
            data = {
                "grant_type": "client_credentials",
                "refresh_token": refresh_token
            }
            try:
                request = await EndpointRequest.create('token', data, RequestType.POST)
                response = await request.send()
                access_token = response['access_token']
                await cache.aset("atmos:access_token", access_token, timeout=3600)
                await cache.aset("atmos:access_token:copy", access_token, timeout=5000)
            except Exception as ex:
                print(ex)