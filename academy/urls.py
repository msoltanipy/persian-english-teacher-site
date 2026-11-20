from django.urls import path
from . import views

app_name = "academy"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/<str:slug>/", views.post_detail, name="post_detail"),
    path("booklets/", views.booklet_list, name="booklet_list"),
    path("booklets/<str:slug>/", views.booklet_detail, name="booklet_detail"),
    path("contact/", views.contact_view, name="contact"),
]
