from bot.bot import *
from app.services import *
from app.models import (
    TelegramChannelAccess,
    Subscription,
    Payment,
    SubscriptionPlan
)
from bot.models import Bot_user
from app.services.subscription_service import (
    create_subscription as _create_subscription,
    get_subscription_by_id as _get_subscription_by_id,
    get_next_active_subscription as _get_next_active_subscription
)
from bot.services.referral_service import referrals_count_of_bot_user
from payment.services.card_service import delete_card_of_bot_user, Card, get_card_of_bot_user
from payment.services.atmos.card_api import remove_card_api as _unlink_card_from_atmos
from config import TG_CHANNEL_ID, TG_CHANNEL_INVITE_LINK
from bot.utils.bot_functions import bot
from typing import Tuple
from telegram.ext import ExtBot


async def get_channel_access_of_bot_user(bot_user: Bot_user):
    obj = await TelegramChannelAccess.objects.filter(
        bot_user__id=bot_user.id).afirst()
    return obj


async def give_channel_access(bot_user: Bot_user, subscription: Subscription) -> Tuple[TelegramChannelAccess, bool]:
    """
    Return: (<`TelegramchannelAccess` objects>, <`is created` boolen>)
    """
    obj, created = await TelegramChannelAccess.objects.aget_or_create(
        bot_user=bot_user,
        defaults={
            "subscription": subscription
        }
    )
    return obj, created


async def update_channel_access(old_subscription: Subscription, new_subscription: Subscription):
    bot_user: Bot_user = await old_subscription.get_bot_user
    # disactivate current subscription
    old_subscription.active = False
    await old_subscription.asave()

    # get telegram channel access
    channel_access: TelegramChannelAccess = await TelegramChannelAccess.objects.aget(
        subscription=old_subscription)

    # set new subscription to channel access
    channel_access.subscription = new_subscription
    await channel_access.asave()


async def remove_user_from_channel(subscription: Subscription):
    bot_user = await subscription.get_bot_user
    # kick user from channel without banning
    is_user_banned: bool = await bot.unban_chat_member(
        chat_id=TG_CHANNEL_ID,
        user_id=bot_user.user_id,
    )
    if is_user_banned:
        # get channel access objects
        channel_access = await TelegramChannelAccess.objects.aget(
            bot_user=bot_user)
        # delete channel access
        await channel_access.adelete()

        # deactivate subscription
        subscription.active = False
        await subscription.asave()

        # Cancel a linked card
        card: Card = await get_card_of_bot_user(bot_user)
        unlinked = await _unlink_card_from_atmos(card.card_id, card.token)
        if unlinked == "OK":
            # Delete Card object
            await delete_card_of_bot_user(bot_user)


async def has_channel_access(user_id: int | str) -> bool:
    exists = await TelegramChannelAccess.objects.filter(
        bot_user__user_id=user_id
    ).aexists()
    return exists


async def successfully_payment_and_create_subscription(
        payment: Payment,
        bot: ExtBot = bot, bot_user: Bot_user = None,
        plan: SubscriptionPlan = None):

    if not bot_user:
        bot_user = await payment.get_bot_user
        plan = await payment.get_plan

    # create subscription
    subscription: Subscription = await _create_subscription(
        bot_user, plan, payment
    )
    # create telegram channel access
    await give_channel_access(bot_user, subscription)
    # check referral available of this user
    if referral := await bot_user.get_referral:
        referrer: Bot_user = await referral.get_referrer
        referrals_count = await referrals_count_of_bot_user(referrer, subscribed=True)
        # check for this referral did not give bonus subscription
        if await Subscription.objects.filter(referral__id=referral.id).aexists():
            # dont give bonus
            pass
        # dont give bonus if referrals count is even of referrer
        elif referrals_count % 2 == 0:
            # create unactive subscription
            await Subscription.objects.acreate(
                bot_user=referrer, referral=referral, active=False
            )
            pass
        else:
            # give bonus to referrer
            referrer: Bot_user = await referral.get_referrer
            # create subscription
            subscription: Subscription = await _create_subscription(
                bot_user=referrer,
                referral=referral
            )
            # send notification about that bonus given
            given_bonus = await GetText.on(Text.given_bonus)
            await send_newsletter(bot, referrer.user_id, given_bonus)
            # give telegram channel access to referrer, if doesn't exist
            channel_access, created = await give_channel_access(referrer, subscription)
            if created:
                joined_to_channel_text = await GetText.on(Text.joined_to_channel)
                markup = ReplyKeyboardMarkup(
                    [[await get_word('main menu', chat_id=bot_user.user_id)]],
                    resize_keyboard=True)
                try:
                    await bot.send_message(referrer.user_id, joined_to_channel_text, reply_markup=markup)
                except:
                    None
    # send video instruction
    try:
        settings = await get_settings()
        i_rules = InlineKeyboardButton(
            text="📝 Klub qonun-qoidalari", url=settings.channel_rules_url)
        await bot.send_video(
            bot_user.user_id,
            settings.instruction_of_channel_video_id,
            reply_markup=InlineKeyboardMarkup([[i_rules]])
        )
    except:
        None

    text = "✅ To'lovingiz muvaffaqiyatli qabul qilindi."
    main_menu_markup = ReplyKeyboardMarkup(
        [[await get_word('main menu', chat_id=bot_user.user_id)]],
        resize_keyboard=True)

    await bot.send_message(bot_user.user_id, text, reply_markup=main_menu_markup)

    text = await GetText.on(Text.joined_to_channel)
    join_channel_markup = InlineKeyboardButton(
        text=await get_word("join channel", chat_id=bot_user.user_id),
        url=TG_CHANNEL_INVITE_LINK
    )
    await bot.send_message(bot_user.user_id, text, reply_markup=join_channel_markup)
