from django.db import models
from django.conf import settings


class ReleaseSchedule(models.Model):
    PRIORITY_CHOICES = [
        ("critical", "critical"),
        ("very_important", "very_important"),
        ("important", "important"),
        ("normal", "normal"),
        ("not_important", "not_important"),
    ]

    date = models.DateField()
    description = models.CharField(max_length=255)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal"
    )

    def __str__(self):
        return f"{self.date}: {self.description}"


class Announcement(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title