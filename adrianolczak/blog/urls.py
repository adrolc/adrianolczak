from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("tag/<slug:slug>/", views.PostListView.as_view(), name="post_list_by_tag"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]
