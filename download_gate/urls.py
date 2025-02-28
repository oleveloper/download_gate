from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts import views as account_views
from files import views as file_views
from . import views

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("management.urls")),
    path('api/csrf/', account_views.get_csrf_token),
    path('api/update/', account_views.update_user),

    path('api/user/', account_views.user_info),
    path('api/signout/', account_views.signout_view, name='signout'),
    path('api/signin/', account_views.signin, name='signin'),
    path('api/signup/', account_views.signup, name='signup'),
    path('api/check-auth/', account_views.check_auth, name='check-auth'),

    path('api/<filetype>/versions/<version>/', file_views.get_files_by_version, name='get-files-by-version'),
    path('api/<filetype>/', file_views.get_version_and_file, name='get-version-and-file'),

    path('', views.index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)