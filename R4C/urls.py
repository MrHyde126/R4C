from django.contrib import admin
from django.urls import include, path

from robots.views import produce_robot

api_v1_urls = [
    path('produce-robot', produce_robot, name='produce_robot'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_urls)),
]
