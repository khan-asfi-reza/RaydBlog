from django.urls import path
from Apps.Users.views.user import UserCreateView, UserProfileRetrieveView, UserProfileListView
from Apps.Users.views.forget_reset_password import ChangePasswordAPI, ResetPasswordAPI, ResetPasswordLinkVerificationAPI, \
    ResetPasswordRequestAPI
from Apps.Users.views.profile import FollowerListView, FollowingListView, FollowUnfollowCreateView, ProfileUpdateView


urlpatterns = [

    # User Creation
    path("create", UserCreateView.as_view(), name="user-create"),
    # Password Reset and Change
    path("password/change", ChangePasswordAPI.as_view(), name="password-change"),
    path("password/forget", ResetPasswordRequestAPI.as_view(), name="password-forget"),
    path("password/validate-reset", ResetPasswordLinkVerificationAPI.as_view(), name="password-validate-reset"),
    path("password/reset", ResetPasswordAPI.as_view(), name="password-reset"),
    # Profile
    path("profiles/", UserProfileListView.as_view(), name="profile-list"),
    path("profile/<int:id>", UserProfileRetrieveView.as_view(), name="profile-get"),
    path("profile/<int:user_id>/edit", ProfileUpdateView.as_view(), name="profile-edit"),
    # Follower List
    path("followers/<int:followee_id>", FollowerListView.as_view(), name="follower-list"),
    path("following/<int:follower_id>", FollowingListView.as_view(), name="following-list"),
    # Follow Unfollow
    path("follow-unfollow/", FollowUnfollowCreateView.as_view(), name="follow-unfollow")
]


