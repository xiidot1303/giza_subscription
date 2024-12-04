from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, admin_views
)

urlpatterns = [
    path('', main.main),

    # admin
    path('export-payments', admin_views.export_payments_to_excel, name="export_payments"),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),



]
