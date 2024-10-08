"""
URL configuration for dicussion_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [
    path("", BoardListView.as_view(), name="home"),
    path("boards/<int:id>", board_topics, name="board_topics"),
    path("boards/<int:id>/new", new_topic, name="new_topic"),
    path("boards/<int:id>/topics/<int:topic_id>", topic_posts, name="topic_posts"),
    path(
        "boards/<int:id>/topics/<int:topic_id>/reply", reply_topic, name="reply_topic"
    ),
    path(
        "boards/<int:id>/topics/<int:topic_id>/posts/<int:post_id>/edit",
        PostUpdateView.as_view(),
        name="edit_post",
    ),
    path("about/", about, name="about"),
]
