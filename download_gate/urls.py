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
    path('api/', include(router.urls)),
    path('api/user/', account_views.user_info),
    path('api/signout/', account_views.signout_view, name='signout'),
    path('api/signin/', account_views.signin, name='signin'),
    path('api/signup/', account_views.signup, name='signup'),
    path('api/check-auth/', account_views.check_auth, name='check_auth'),
    path('api/install/version/', file_views.versions, name='install-file-versions'),
    path('api/install/version/<version>/files/', file_views.version_files, name='install-files'),
    path('api/<filetype>/files/', file_views.files, name='files'),
    path('', views.index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)