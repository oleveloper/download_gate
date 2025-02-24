from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ReleaseSchedule, Announcement
from .serializers import ReleaseScheduleSerializer, AnnouncementSerializer


@api_view(["GET"])
def get_release_schedule(request):
    schedules = ReleaseSchedule.objects.order_by("-date")
    serializer = ReleaseScheduleSerializer(schedules, many=True)
    return Response({"release_schedule": serializer.data})


@api_view(["GET"])
def get_announcements(request):
    announcements = Announcement.objects.order_by("-date")
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response({"announcements": serializer.data})


@api_view(["GET"])
def get_dashboard_data(request):
    schedules = ReleaseSchedule.objects.order_by("date")
    announcements = Announcement.objects.order_by("-date")

    schedule_serializer = ReleaseScheduleSerializer(schedules, many=True)
    announcement_serializer = AnnouncementSerializer(announcements, many=True)

    return Response({
        "release_schedule": schedule_serializer.data,
        "announcements": announcement_serializer.data
    })