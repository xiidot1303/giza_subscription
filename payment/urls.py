from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from payment.views import (
    payme, subscribe
)

urlpatterns = [
    # payme
    path('payme/endpoint', payme.Endpoint.as_view()),

    # subscribe
    path('subscribe/set-card', subscribe.set_card),
    path('cards/init', subscribe.InitCardView.as_view()),
    path('cards/confirm', subscribe.CofirmCardView.as_view()),

    path('cards/create', subscribe.CreateCardView.as_view()),
    path('cards/getverifycode', subscribe.GetVerifyCodeView.as_view()),
    path('cards/verify', subscribe.VerifyView.as_view()),
]
