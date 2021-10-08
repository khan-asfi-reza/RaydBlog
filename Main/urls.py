from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from Main import settings
from Main.settings import DEBUG

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('api/users/', include("Apps.Users.urls")),
                  path('api/auth/', include("Apps.Authentication.urls")),

                  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
                  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

              ]

if DEBUG:
    def test_html_view(request):
        return render(request, "index.html")

    urlpatterns += path('/test/doc', test_html_view, name="test-html")