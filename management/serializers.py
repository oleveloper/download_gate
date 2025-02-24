from rest_framework import serializers
from .models import ReleaseSchedule, Announcement


class ReleaseScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReleaseSchedule
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Announcement
        fields = "__all__"
