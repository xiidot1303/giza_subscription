from django.urls import path, re_path
from config import BOT_API_TOKEN
from django.conf import settings
from config import DEBUG
from django.conf.urls.static import static
from bot.views import botwebhook, profile, referral, admin_views

urlpatterns = [
    path(BOT_API_TOKEN, botwebhook.BotWebhookView.as_view()),

    # profile
    path("profile/<str:id>/", profile.home),
    path("profile/update-card", profile.UpdateCard.as_view()),

    # subscription
    path("subscription/cancel", profile.CancelSubscription.as_view()),

    # referral
    path('referral/<str:id>/', referral.main),

    # admin
    path('export-bot_users', admin_views.export_bot_users_to_excel, name='export_bot_users'),
]