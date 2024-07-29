from django.urls import path
from .views import post_list, post_detail, comment_list_create, comment_delete

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/<int:post_id>/comments/', comment_list_create, name='comment-list-create'),
    path('comments/<int:comment_id>/delete/', comment_delete, name='comment-delete'),
]
