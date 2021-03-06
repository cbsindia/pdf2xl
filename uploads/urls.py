from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views
from downloads.views import *


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/$', views.simple_upload, name='simple_upload'),
    url(r'^api/uploads/$', views.api_upload, name='api_upload'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^download/(?P<in_file>\S+)/$', download, name='file_download'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
