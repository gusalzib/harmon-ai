from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("set-csrf-cookie", views.set_csrf_cookie, name="set-csrf-cookie"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("get-preferences", views.get_user_preferences, name="get-preferences"),
    path("profile", views.get_user_info, name="profile"),
    path("change-password", views.change_password, name="change-password"),
    path("edit-profile", views.edit_profile, name="edit-profile"),
    path("check-status", views.check_status, name="check_status"),
    path("admin-upload", views.upload_dataset, name="upload_dataset"),
]