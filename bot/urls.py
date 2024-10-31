from django.urls import path, re_path
from config import BOT_API_TOKEN
from django.conf import settings
from config import DEBUG
from django.conf.urls.static import static
from bot.views import botwebhook, profile

urlpatterns = [
    path(BOT_API_TOKEN, botwebhook.BotWebhookView.as_view()),

    path("profile/<int:id>/", profile.home),
    path("profile/update-card", profile.UpdateCard.as_view()),
]