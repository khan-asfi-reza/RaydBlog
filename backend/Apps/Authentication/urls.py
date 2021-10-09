from django.urls import path

from Apps.Authentication.views.authentication import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Token Obtain and Refresh
    path("token", TokenObtainPairView.as_view(), name="jwt-obtain"),
    path("token/refresh", TokenRefreshView.as_view(), name="jwt-refresh"),
]