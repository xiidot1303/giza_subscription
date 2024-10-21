from bot.services.language_service import get_word
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)


async def _inline_footer_buttons(update, buttons, back=True, main_menu=True):
    new_buttons = []
    if back:
        new_buttons.append(
            InlineKeyboardButton(text=get_word('back', update), callback_data='back'),
        )
    if main_menu:
        new_buttons.append(
            InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu'),
        )

    buttons.append(new_buttons)
    return buttons

async def select_lang_keyboard():
    buttons = [["UZ 🇺🇿", "RU 🇷🇺"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return markup

async def settings_keyboard(update):

    buttons = [
        [get_word("change lang", update)],
        [get_word("change name", update)],
        [get_word("change phone number", update)],
        [get_word("main menu", update)],
    ]

    return buttons

async def build_keyboard(update, button_list, n_cols, back_button=True, main_menu_button=True):
    # split list by two cols
    button_list_split = [button_list[i:i + n_cols] for i in range(0, len(button_list), n_cols)]
    # add buttons back and main menu
    footer_buttons = []
    if back_button:
        footer_buttons.append(
            await get_word('back', update)
        )
    if main_menu_button:
        footer_buttons.append(
            await get_word('main menu', update)
        )
    # add footer buttons if available
    buttons = button_list_split + [footer_buttons] if footer_buttons else button_list_split

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return reply_markup