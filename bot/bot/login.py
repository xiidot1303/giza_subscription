from bot.bot import *
from bot.services.referral_service import *


async def _to_the_getting_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_message_reply_text(
        update,
        await get_word("type name", update),
        reply_markup=await reply_keyboard_remove()
    )
    return GET_NAME


async def _to_the_getting_contact(update: Update):
    i_contact = KeyboardButton(
        text=await get_word("leave number", update),
        request_contact=True
    )

    await update_message_reply_text(
        update,
        await get_word("send number", update),
        reply_markup=await reply_keyboard_markup(
            [[i_contact], [await get_word("back", update)]], one_time_keyboard=True
        )
    )

    return GET_CONTACT

###################################################################################
###################################################################################


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    return await _to_the_getting_contact(update)


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get phone number from message
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    # get name from user data
    name = context.user_data['name']
    # get referrer_id from user data
    start_msg = context.user_data.get('start_msg', None)
    referrer_id, utm_source = None, None
    if start_msg:
        if "referrer" in start_msg:
            _, referrer_id = start_msg.split("--")
            utm_source = "referral"
        else:
            utm_source = start_msg

    # create bot user
    bot_user, created = await Bot_user.objects.aget_or_create(
        user_id=context._user_id,
        defaults={
            "name": name,
            "firstname": update.effective_user.first_name,
            "username": update.effective_user.username,
            "phone": phone_number,
            "utm_source": utm_source
        }
    )

    # create referral if user has referrer
    if referrer_id:
        # get referrer object
        if referrer := await get_object_by_pk(referrer_id):
            # create Referral
            await create_referral(bot_user, referrer)

    await main_menu(update, context)
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await _to_the_getting_name(update, context)
