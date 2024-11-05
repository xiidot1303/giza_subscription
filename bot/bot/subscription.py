from bot.bot import *
from app.services.subscription_service import *
from app.services.channel_access_service import *


async def cancel_subscription(update: Update, context: CustomContext):
    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context)
    
    *args, subscription_id = str(update.callback_query.data).split("--")
    subscription: Subscription = await get_subscription_by_id(subscription_id)
    
    # cancel subscription
    await deactivate_subscription_and_update_channel_access(subscription)