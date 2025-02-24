from django.contrib import admin
from .models import ReleaseSchedule, Announcement


@admin.register(ReleaseSchedule)
class ReleaseScheduleAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "priority")
    list_filter = ("priority",)
    ordering = ("-date",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("date", "author", "title")
    ordering = ("-date",)