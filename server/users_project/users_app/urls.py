from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("set-csrf-cookie", views.set_csrf_cookie, name="set-csrf-cookie"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("profile", views.get_user_info, name="profile"),
    path("change-password", views.change_password, name="change-password")
]