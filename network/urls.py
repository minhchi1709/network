
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("user/<int:id>", views.user, name='user'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('following', views.following, name='following'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('like/<int:id>', views.like, name='edit'),
    path('comment/<int:id>', views.comment, name='comment'),
]
