from django.urls import path
from .views import HomeView

app_name = "mainapp"

urlpatterns = [
    path('', HomeView.as_view() , name="home"),
]

