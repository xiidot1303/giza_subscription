from bot.bot import *


async def _to_the_getting_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_message_reply_text(
        update,
        await get_word("type name", update),
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
            [[i_contact], [await get_word("back", update)]],
        )
    )

    return GET_CONTACT

###################################################################################
###################################################################################


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    obj = await get_object_by_update(update)
    obj.name = update.message.text
    obj.username = update.message.chat.username
    obj.firstname = update.message.chat.first_name
    await obj.asave()

    return await _to_the_getting_contact(update)


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get phone number from message
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    # check phone number is registred in the past or not
    is_available = await filter_objects_sync(Bot_user, {'phone': phone_number})
    if is_available:
        await update.message.reply_text(
            await get_word("number is logged", update)
        )
        return GET_CONTACT

    obj = await get_object_by_update(update)
    obj.phone = phone_number
    await obj.asave()

    await main_menu(update, context)
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await _to_the_getting_name(update, context)
