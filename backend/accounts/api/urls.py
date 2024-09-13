from django.urls import path
from .views import LoginView, UserProfileView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("register/", RegisterView.as_view(), name="regster"),
]
