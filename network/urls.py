
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    # path("profile", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #API Paths
    path("all", views.all, name="all"),
    path("posts", views.posts, name="posts"),
    path("profile/<str:user>/posts", views.userposts, name="userposts"),
    # path("profile/<str:following", views.followingposts, name="followingposts"),
]
