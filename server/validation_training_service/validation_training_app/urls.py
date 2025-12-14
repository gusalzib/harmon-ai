from django.urls import path
from . import views

urlpatterns = [
    path("train/", views.test_train_model, name="test_train_model"),
    path("report/", views.fetch_reports, name="fetch_reports")

]
