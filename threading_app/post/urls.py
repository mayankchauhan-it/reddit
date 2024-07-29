from django.urls import path
from .views import publish_post, home, post_detail

urlpatterns = [
    path('', home, name='home'),
    path('publish/', publish_post, name='publish_post'),
    path('<int:pk>/', post_detail, name='post_detail'),
]
