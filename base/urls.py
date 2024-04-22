from django.urls import path
from base import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),

]