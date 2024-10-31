from bot.bot import *
import json
from app.services.payment_service import *
from app.services.plan_service import *
from app.services.subscription_service import *
from app.services.channel_access_service import *
from payment.services.payme.subscribe_api import *
from payment.services.card_service import *
from config import DEBUG


async def web_app_data(update: Update, context: CustomContext) -> None:
    # get data from web app data
    data = json.loads(update.effective_message.web_app_data.data)
    token = data["token"]
    plan_id = context.user_data["plan_id"]
    channel_id = context.user_data["channel_id"]
    # get subscription plan object
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)
    # get bot user by update
    bot_user: Bot_user = await get_user_by_update(update)

    # create payment
    payment: Payment = await create_payment(bot_user, plan.price)
    # create receipt
    receipt_id = await receipts_create_api(payment.id, payment.amount)
    # pay receipt
    receipt_pay_data = await receipts_pay_api(receipt_id, token)
    # update payment object because it changed by merchant api
    await payment.arefresh_from_db()
    
    if DEBUG:
        payment.payed = True
        await payment.asave()

    if "result" in receipt_pay_data and payment.payed:
        # successfullt payment, approve channel join request

        # create or update card of the user
        card_info = DictToClass(receipt_pay_data["result"]["receipt"]["card"])
        card_info.token = token
        await update_card_of_bot_user(bot_user, card_info)

        # create subscription
        subscription: Subscription = await create_subscription(
            bot_user, plan, payment
        )

        # approve channel join request
        await context.bot.approveChatJoinRequest(
            chat_id=channel_id,
            user_id=bot_user.user_id
        )

        # create telegram channel access
        await give_channel_access(bot_user, subscription)
        
        text = await GetText.on(Text.joined_to_channel)
        await update_message_reply_text(update, text, reply_markup=await reply_keyboard_remove())

    elif "error" in receipt_pay_data:
        # error in payment
        text = await GetText.on(Text.error_in_payment)
        await update_message_reply_text(update, text)
