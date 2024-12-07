from bot.services.language_service import get_word
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from config import WEBAPP_URL
from app.services.plan_service import subscription_plans_filter_dict, SubscriptionPlan


async def _inline_footer_buttons(update, buttons, back=True, main_menu=True):
    new_buttons = []
    if back:
        new_buttons.append(
            InlineKeyboardButton(text=get_word(
                'back', update), callback_data='back'),
        )
    if main_menu:
        new_buttons.append(
            InlineKeyboardButton(text=get_word(
                'main menu', update), callback_data='main_menu'),
        )

    buttons.append(new_buttons)
    return buttons


async def select_lang_keyboard():
    buttons = [["UZ 🇺🇿", "RU 🇷🇺"]]
    markup = ReplyKeyboardMarkup(
        buttons, resize_keyboard=True, one_time_keyboard=True)
    return markup


async def settings_keyboard(update):

    buttons = [
        [get_word("change lang", update)],
        [get_word("change name", update)],
        [get_word("change phone number", update)],
        [get_word("main menu", update)],
    ]

    return buttons


async def build_keyboard(
    update, button_list, n_cols, back_button=True,
    main_menu_button=True, one_time_keyboard=True
):
    # split list by two cols
    button_list_split = [button_list[i:i + n_cols]
                         for i in range(0, len(button_list), n_cols)]
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
    buttons = button_list_split + \
        [footer_buttons] if footer_buttons else button_list_split

    reply_markup = ReplyKeyboardMarkup(
        buttons, resize_keyboard=True, one_time_keyboard=one_time_keyboard)
    return reply_markup


async def cancel_subscription_keyboard(subscription_id):
    i_confirm = InlineKeyboardButton(
        text="Tasdiqlayman",
        callback_data=f"cancel_subscription--{subscription_id}"
    )
    i_no = InlineKeyboardButton(
        text="Yo'q",
        callback_data="delete_current_message"
    )

    markup = InlineKeyboardMarkup([[i_confirm, i_no]])
    return markup


async def change_card_keyboard(bot_user):
    i_button = InlineKeyboardButton(
        text=await get_word("edit card", chat_id=bot_user.user_id),
        web_app=WebAppInfo(f"{WEBAPP_URL}/profile/{bot_user.id}")
    )
    markup = InlineKeyboardMarkup([[i_button]])
    return markup


async def survey_options_keyboard():
    i_buttons = [
        [InlineKeyboardButton(
            text=option,
            callback_data=f"survey--{option}"
        )]
        for option in ["Pul", "Sog'liq", "Munosabatlar"]
    ]

    return InlineKeyboardMarkup(i_buttons)


async def tariffs_list_keyboard():
    i_tariff_buttons = [
        [
            InlineKeyboardButton(
                text=plan.name,
                callback_data=f"subscription_plan--{plan.id}"
            )
        ]
        async for plan in SubscriptionPlan.objects.filter(
            **subscription_plans_filter_dict).order_by("duration_in_months")
    ]
    markup = InlineKeyboardMarkup(i_tariff_buttons)
    return markup