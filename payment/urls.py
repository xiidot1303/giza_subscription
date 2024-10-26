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
    path('payme/endpoint', payme.endpoint),

    # subscribe
    path('subscribe/set-card', subscribe.set_card),
    path('cards/create', subscribe.create_card),
    path('cards/getverifycode', subscribe.get_verify_code),
    path('cards/verify', subscribe.verify),
]
