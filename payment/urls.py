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
    path('set-card', subscribe.set_card)
]
