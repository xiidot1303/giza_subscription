from bot.bot import *
from app.services.subscription_service import *
from app.services.channel_access_service import *


async def cancel_subscription(update: Update, context: CustomContext):
    # remove inline keyboards
    await bot_edit_message_reply_markup(update, context)
    
    *args, subscription_id = str(update.callback_query.data).split("--")
    subscription: Subscription = await get_subscription_by_id(subscription_id)
    bot_user: Bot_user = await subscription.get_bot_user
    
    # cancel subscription
    # if active subcriptions available in the next, set subscription or remove user from channel
    if next_subscription := await get_next_active_subscription(subscription):
        await update_channel_access(subscription, next_subscription)
        # send message about subscription changed
        expire_date = next_subscription.end_date.strftime("%d.%m.%Y")
        text = await your_subscription_changed_string(
            await subscription.get_plan_name,
            await next_subscription.get_plan_name,
            expire_date
        )
        await update_message_reply_text(update, text)
    else:
        await remove_user_from_channel(subscription)
        # send message about successfully deactivated subscription
        text = await get_word('successfully deactivated subscription', update)
        await update_message_reply_text(update, text)