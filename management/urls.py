from django.urls import path
from .views import get_release_schedule, get_announcements, get_dashboard_data

urlpatterns = [
    path("release-schedule/", get_release_schedule, name="release-schedule"),
    path("announcements/", get_announcements, name="announcements"),
    path("", get_dashboard_data, name="dashboard-data"),
]