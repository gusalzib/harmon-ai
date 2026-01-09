from django.urls import path
from . import views

urlpatterns = [
    path("train/", views.test_train_model, name="test_train_model"),
    path("report/", views.fetch_reports, name="fetch_reports"),
    path("update/", views.update_model_name, name="update_model_name")

]
