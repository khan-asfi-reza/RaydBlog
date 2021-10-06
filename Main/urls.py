
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Main import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/users/', include("Apps.Users.urls")),
                  path('api/auth/', include("Apps.Authentication.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
